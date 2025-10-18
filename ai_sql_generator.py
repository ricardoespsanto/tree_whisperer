"""AI SQL generator module for Tree Whisperer application."""

import re
from typing import Dict, List, Tuple

import openai
import sqlparse
from config import Config

class AISQLGenerator:
    """AI SQL generator for Tree Whisperer application."""

    def __init__(self):
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL

        # Database schema context for the AI
        self.schema_context = """
        Database Schema for Tree and Forest Data:

        Tables:
        1. tree_species: Contains information about different tree species
           - id, scientific_name, common_name, family, genus, species
           - native_region, max_height_meters, max_diameter_cm, lifespan_years
           - growth_rate, wood_density

        2. forest_regions: Contains information about forest areas
           - id, region_name, country, state_province, latitude, longitude
           - area_hectares, forest_type, climate_zone, elevation_meters

        3. forest_inventory: Tracks trees in specific forests over time
           - forest_region_id, tree_species_id, year_recorded, tree_count
           - average_height_meters, average_diameter_cm, total_biomass_kg
           - carbon_storage_kg, health_status

        4. logging_records: Records of tree harvesting
           - forest_region_id, tree_species_id, year_logged, trees_logged
           - volume_cubic_meters, value_usd, logging_type, sustainability_certification

        5. forest_growth: Tracks forest area changes over time
           - forest_region_id, year_measured, total_area_hectares
           - forest_cover_percentage, net_growth_hectares, deforestation_hectares
           - reforestation_hectares, carbon_sequestration_tonnes, biodiversity_index
        """

        self.system_prompt = f"""
        You are an AI assistant specialized in generating SQL queries for a tree and forest database.
        Your role is to convert natural language questions about trees, forests, and ecosystems into accurate SQL queries.

        {self.schema_context}

        IMPORTANT RULES:
        1. You can ONLY generate SELECT statements - no INSERT, UPDATE, DELETE, DROP, or other modifying operations
        2. You must stay strictly within the domain of trees, forests, ecosystems, and related environmental data
        3. If a question is not related to trees/forests, respond with: "I can only answer questions about trees, forests, and ecosystems. Please ask about forest data, tree species, logging records, or forest growth."
        4. Always use proper JOINs when querying related tables
        5. Use appropriate WHERE clauses to filter data
        6. Include ORDER BY clauses when ranking or finding extremes
        7. Use aggregate functions (COUNT, SUM, AVG, MAX, MIN) when appropriate
        8. Be precise with column names and table names as shown in the schema

        Response format:
        1. First, explain your reasoning for the query
        2. Then provide the SQL query
        3. Finally, suggest what the query results might show
        """

    def is_tree_forest_related(self, question: str) -> bool:
        """Check if the question is related to trees, forests, or ecosystems"""
        tree_forest_keywords = [
            'tree', 'trees', 'forest', 'forests', 'wood', 'woods', 'timber', 'lumber',
            'oak', 'pine', 'maple', 'fir', 'cedar', 'spruce', 'hemlock', 'beech',
            'redwood', 'sequoia', 'logging', 'harvest', 'deforestation', 'reforestation',
            'carbon', 'biomass', 'biodiversity', 'ecosystem', 'species', 'genus',
            'height', 'diameter', 'growth', 'age', 'lifespan', 'density', 'volume',
            'region', 'climate', 'elevation', 'area', 'hectares', 'acres'
        ]

        question_lower = question.lower()
        return any(keyword in question_lower for keyword in tree_forest_keywords)

    def validate_sql(self, sql: str) -> Tuple[bool, str]:
        """Validate that the SQL is safe and only contains SELECT statements"""
        try:
            # Parse the SQL to check for dangerous operations
            parsed = sqlparse.parse(sql)

            for statement in parsed:
                # Check if it's a SELECT statement
                if not statement.get_type() == 'SELECT':
                    return False, "Only SELECT statements are allowed"

                # Check for dangerous keywords
                dangerous_keywords = [
                    'insert', 'update', 'delete', 'drop', 'create', 'alter',
                    'truncate', 'grant', 'revoke', 'exec', 'execute', 'sp_'
                ]

                sql_lower = sql.lower()
                for keyword in dangerous_keywords:
                    if keyword in sql_lower:
                        return False, f"Dangerous keyword '{keyword}' detected"

            return True, "SQL is valid"

        except (AttributeError, ValueError) as e:
            return False, f"SQL parsing error: {str(e)}"

    def generate_sql(self, question: str, conversation_history: List[Dict] = None) -> Dict:
        """Generate SQL query from natural language question"""

        # Check if question is tree/forest related
        if not self.is_tree_forest_related(question):
            return {
                'success': False,
                'error': 'I can only answer questions about trees, forests, and ecosystems. ' \
                'Please ask about forest data, tree species, logging records, or forest growth.',
                'sql': None,
                'explanation': None
            }

        # Build conversation context
        messages = [{"role": "system", "content": self.system_prompt}]

        if conversation_history:
            for msg in conversation_history[-5:]:  # Last 5 messages for context
                messages.append(msg)

        messages.append({"role": "user", "content": question})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.1,  # Low temperature for consistent SQL generation
                max_tokens=1000
            )

            ai_response = response.choices[0].message.content

            # Extract SQL from the response
            sql_match = re.search(r'```sql\s*(.*?)\s*```', ai_response, re.DOTALL | re.IGNORECASE)
            if not sql_match:
                # Try to find SQL without code blocks
                sql_match = re.search(
                    r'(SELECT\s+.*?)(?:\n\n|\Z)', ai_response, re.DOTALL | re.IGNORECASE
                )

            if not sql_match:
                return {
                    'success': False,
                    'error': 'Could not extract SQL query from AI response',
                    'sql': None,
                    'explanation': ai_response
                }

            sql_query = sql_match.group(1).strip()

            # Validate the SQL
            is_valid, validation_message = self.validate_sql(sql_query)

            if not is_valid:
                return {
                    'success': False,
                    'error': f'Invalid SQL generated: {validation_message}',
                    'sql': sql_query,
                    'explanation': ai_response
                }

            return {
                'success': True,
                'sql': sql_query,
                'explanation': ai_response,
                'error': None
            }

        except (AttributeError, ValueError) as e:
            return {
                'success': False,
                'error': f'Error generating SQL: {str(e)}',
                'sql': None,
                'explanation': None
            }

    def format_response(self, sql_result: List[Dict]) -> str:
        """Format the final response for the user"""
        if not sql_result:
            return ("I found no data matching your query. The database may not contain "
                    "information for the specific criteria you mentioned.")

        # Create a summary based on the results
        if len(sql_result) == 1:
            result = sql_result[0]
            if len(result) == 1:
                # Single value result
                value = list(result.values())[0]
                return f"Based on the database, {value}."
            # Single row result
            summary = ", ".join([f"{k}: {v}" for k, v in result.items()])
            return f"Here's what I found: {summary}."


        # Multiple results
        if len(sql_result) <= 10:
            # Show all results
            summaries = []
            for i, result in enumerate(sql_result, 1):
                summary = ", ".join([f"{k}: {v}" for k, v in result.items()])
                summaries.append(f"{i}. {summary}")
            return f"I found {len(sql_result)} results:\n" + "\n".join(summaries)

        # Show first few and count
        summaries = []
        for i, result in enumerate(sql_result[:5], 1):
            summary = ", ".join([f"{k}: {v}" for k, v in result.items()])
            summaries.append(f"{i}. {summary}")
        return (f"I found {len(sql_result)} results. Here are the first 5:\n" + "\n".
        join(summaries) +f"\n... and {len(sql_result) - 5} more results.")
