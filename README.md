# 🌲 Tree Whisperer - AI Forest Data Assistant

An AI-powered chatbot that answers questions about trees, forests, and ecosystems by querying a SQL database. Built with Python, Flask, OpenAI GPT, and MySQL.

## 🚀 Features

- **Natural Language to SQL**: Convert questions about trees and forests into SQL queries
- **Read-Only Database Access**: Secure, read-only access to forest data
- **AI-Powered Responses**: Uses OpenAI GPT to generate and explain SQL queries
- **Rate Limiting**: Built-in protection against abuse with configurable limits
- **Modern Web Interface**: Clean, responsive chat interface
- **Real-time Usage Stats**: Monitor daily query usage and limits
- **Docker Deployment**: Easy deployment with Docker Compose
- **Security First**: Input sanitization, SQL validation, and safety guardrails

## 📊 Database Schema

The application works with a comprehensive forest database containing:

- **Tree Species**: Scientific names, common names, growth characteristics
- **Forest Regions**: Geographic locations, climate zones, forest types
- **Forest Inventory**: Tree counts, biomass, carbon storage by region and time
- **Logging Records**: Harvesting data, sustainability certifications
- **Forest Growth**: Area changes, deforestation, reforestation tracking

## 🛠️ Technology Stack

- **Backend**: Python 3.11, Flask
- **AI**: OpenAI GPT-3.5 Turbo
- **Database**: MySQL 8.0
- **Caching**: Redis
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Docker, Docker Compose, Nginx
- **Hosting**: DigitalOcean (recommended)

## 📋 Prerequisites

- Docker and Docker Compose
- OpenAI API key
- DigitalOcean account (for hosting)
- Domain name (optional, for production)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd tree_whisperer
```

### 2. Configure Environment

Create a `.env` file with your configuration:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_here

# Optional (defaults provided)
DB_HOST=localhost
DB_PORT=3306
DB_NAME=tree_whisperer
DB_USER=tree_user
DB_PASSWORD=secure_password_change_me
RATE_LIMIT_PER_MINUTE=1
DAILY_QUERY_LIMIT=100
```

### 3. Deploy with Docker

```bash
# Make deployment script executable
chmod +x deploy.sh

# Deploy (requires OPENAI_API_KEY and SECRET_KEY environment variables)
OPENAI_API_KEY=your_key SECRET_KEY=your_secret ./deploy.sh
```

### 4. Access the Application

- **Web Interface**: http://your-server-ip
- **Health Check**: http://your-server-ip/api/health
- **API Documentation**: http://your-server-ip/api/schema

## 🔧 Development Setup

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set up MySQL database
mysql -u root -p < database/schema.sql
mysql -u root -p < database/sample_data.sql

# Run the application
python app.py
```

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📖 API Endpoints

### Chat API
- **POST** `/api/chat` - Send a question and get AI response
- **GET** `/api/health` - Health check endpoint
- **GET** `/api/usage` - Get usage statistics
- **GET** `/api/schema` - Get database schema information

### Example API Usage

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the tallest tree species?", "user_id": "user123"}'
```

## 🎯 Example Questions

The AI can answer questions like:

- "What is the tallest tree species in the database?"
- "How many white oaks were logged in Maine last year?"
- "Which forest region has the highest carbon storage?"
- "Compare the growth rates of pine species"
- "What is the total area of forests in the database?"
- "Show me deforestation trends over the last 3 years"

## 🔒 Security Features

- **Read-Only Database**: Only SELECT queries allowed
- **Input Validation**: SQL injection prevention
- **Rate Limiting**: Per-minute and daily limits
- **Domain Restriction**: Only answers tree/forest questions
- **SQL Validation**: Automatic query safety checks
- **Usage Monitoring**: Real-time usage tracking and alerts

## 📊 Monitoring and Logs

### View Logs
```bash
# Application logs
docker-compose logs -f app

# All services
docker-compose logs -f

# Database logs
docker-compose logs -f mysql
```

### Health Monitoring
- Health check endpoint: `/api/health`
- Usage statistics: `/api/usage`
- Database connection status included in health checks

## 🚀 DigitalOcean Deployment

### 1. Create Droplet
- Choose Ubuntu 22.04 LTS
- Minimum 2GB RAM, 1 CPU
- Add SSH key for access

### 2. Install Docker
```bash
# On your DigitalOcean droplet
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo usermod -aG docker $USER
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 3. Deploy Application
```bash
# Clone and deploy
git clone <your-repo>
cd tree_whisperer
OPENAI_API_KEY=your_key SECRET_KEY=your_secret ./deploy.sh
```

### 4. Configure Domain (Optional)
- Point your domain to the droplet IP
- Update nginx.conf with your domain name
- Add SSL certificates to ./ssl/ directory
- Restart nginx: `docker-compose restart nginx`

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (required) | - |
| `SECRET_KEY` | Flask secret key (required) | - |
| `DB_HOST` | MySQL host | localhost |
| `DB_PORT` | MySQL port | 3306 |
| `DB_NAME` | Database name | tree_whisperer |
| `DB_USER` | Database user | tree_user |
| `DB_PASSWORD` | Database password | - |
| `RATE_LIMIT_PER_MINUTE` | API rate limit | 1 |
| `DAILY_QUERY_LIMIT` | Daily query limit | 100 |
| `REDIS_URL` | Redis connection URL | redis://localhost:6379/0 |

### Rate Limiting

- **Per-minute limit**: 1 query per IP address
- **Daily limit**: 100 queries total (configurable)
- **Email alerts**: Sent at 80% of daily limit
- **Cooldown**: 5-second cooldown in UI

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check MySQL is running: `docker-compose ps mysql`
   - Verify credentials in `.env`
   - Check logs: `docker-compose logs mysql`

2. **OpenAI API Errors**
   - Verify API key is correct
   - Check API usage limits
   - Ensure sufficient credits

3. **Rate Limiting Issues**
   - Check Redis is running: `docker-compose ps redis`
   - Verify rate limit settings
   - Clear Redis cache if needed

4. **Application Won't Start**
   - Check all environment variables are set
   - Verify Docker is running
   - Check logs: `docker-compose logs app`

### Debug Mode

Enable debug mode by setting `DEBUG=true` in your `.env` file:

```bash
DEBUG=true docker-compose up
```

## 📈 Performance Optimization

### For Production

1. **Database Optimization**
   - Add indexes for frequently queried columns
   - Optimize MySQL configuration
   - Consider read replicas for high traffic

2. **Caching**
   - Enable Redis caching for common queries
   - Implement query result caching
   - Use CDN for static assets

3. **Scaling**
   - Use multiple app instances behind load balancer
   - Implement database connection pooling
   - Consider microservices architecture

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the troubleshooting section
- Review the logs for error messages
- Open an issue on GitHub
- Contact the development team

## 🔮 Future Enhancements

- [ ] Support for more database types (PostgreSQL, SQLite)
- [ ] Advanced analytics and reporting
- [ ] Multi-language support
- [ ] Voice interface integration
- [ ] Mobile app
- [ ] Advanced visualization tools
- [ ] Machine learning model training on forest data
- [ ] Integration with external forest APIs

---

**Tree Whisperer** - Making forest data accessible through AI-powered natural language queries. 🌲🤖
