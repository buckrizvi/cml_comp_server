# CML Comp Server

A powerful Flask web application for fetching comparable property data from the PRYCD Comps API via RapidAPI. Designed for real estate professionals, investors, and researchers who need quick access to property comparable data with geographic and acreage-based filtering.

🚀 **Now optimized for serverless deployment on Vercel!**

## ✨ Features

### Core Functionality
- 🏡 **Property Comparable Search**: Find similar properties by location, acreage, and other criteria
- 📍 **Geographic Search**: Search by latitude/longitude with customizable radius
- 📊 **Rich Data Export**: Export detailed property data to CSV format
- 🔍 **Advanced Filtering**: Filter by acreage range, property age, and remove duplicates
- 🔐 **Secure Access**: Password-protected interface for authorized users only

### Data Fields Exported
- **Location**: Latitude, Longitude, Address, City
- **Property Details**: Acreage, Price, Price per Acre, Status
- **Metadata**: Source, Distance from search point
- **Additional Info**: Available based on API response

### Developer Features
- 🛠️ **Comprehensive Debugging**: Built-in debug mode shows API requests, responses, and data flow
- 📋 **Environment Variable Validation**: Checks API keys and configuration
- 🔄 **Smart Error Handling**: Detailed error messages and troubleshooting guidance
- ☁️ **Serverless Ready**: Optimized for Vercel's serverless platform
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Local Development

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy environment variables:
   ```bash
   cp env.example .env
   ```
5. Edit `.env` with your actual values:
   - `RAPIDAPI_KEY`: Your RapidAPI key for the property comps service
   - `SECURE_KEY`: A secure key to protect access to your form
6. Run locally:
   ```bash
   python app.py
   ```

## 🚀 Vercel Deployment (Recommended)

This application is optimized for Vercel's serverless platform and can be deployed directly from GitHub.

### Prerequisites
- Vercel account (free hobby plan supported)
- GitHub repository (this one!)

### Quick Deployment Steps

1. **Go to [vercel.com](https://vercel.com)** and sign in with GitHub
2. **Click "New Project"** and import this repository
3. **Vercel will auto-detect** the Python configuration
4. **Set Environment Variables** before deploying:
   - `RAPIDAPI_KEY`: Your RapidAPI key for PRYCD Comps API
   - `SECURE_KEY`: Your chosen password for app access
5. **Click Deploy** - your app will be live in minutes!

### Alternative: CLI Deployment

If you prefer using the command line:

1. **Install Vercel CLI:**
   ```bash
   npm install -g @vercel/cli
   ```

2. **Deploy:**
   ```bash
   vercel --prod
   ```

### Post-Deployment
- Your app will be available at `https://your-project-name.vercel.app`
- Any pushes to the main branch will automatically redeploy
- Monitor logs and performance in the Vercel dashboard

### Project Structure for Vercel

```
cml_comp_server/
├── api/
│   └── index.py          # Main serverless function
├── templates/
│   └── form.html         # HTML template
├── public/
│   └── templates/        # Static files for Vercel
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
├── env.example          # Environment variables template
└── README.md            # This file
```

## 📋 How to Use

### Basic Usage
1. **Access the App**: Navigate to your deployed Vercel URL
2. **Authenticate**: Enter your secure key (set in environment variables)
3. **Set Search Parameters**:
   - **Latitude/Longitude**: Target location coordinates
   - **Acreage Range**: Minimum and maximum property size
   - **Search Radius**: How far to search (in miles, decimals allowed)
   - **Max Comparables**: Maximum number of results (up to API limits)
   - **Property Age**: How recent the comparables should be (in days)
   - **Remove Duplicates**: Filter out similar properties
4. **Get Results**: Click "Get Comps" to download CSV file

### Debug Mode
- **Check the "Show Debug Information" box** to see detailed information about:
  - Environment variable status
  - API request/response details
  - Data processing steps
  - Error diagnostics
- **Perfect for troubleshooting** empty results or API issues

### CSV Output
The exported CSV includes:
- Property location (lat/lng, address, city)
- Property details (acreage, price, price per acre, status)
- Search metadata (distance from search point, data source)

## Environment Variables

- `RAPIDAPI_KEY`: Required. Your RapidAPI key for accessing the property comparables API
- `SECURE_KEY`: Required. A secret key to protect access to your application

## API Integration

This application integrates with the RapidAPI property comparables service:
- Endpoint: `https://prycd-comps.p.rapidapi.com/compsByLatLong`
- Returns property data in JSON format
- Exports results as CSV file

## 🛠️ Troubleshooting

### Using Debug Mode
The built-in debug mode is your best friend for troubleshooting:
1. Check the **"Show Debug Information"** box on the form
2. Submit your search to see detailed diagnostic information
3. Review each section to identify issues

### Common Issues

#### Empty CSV Files
- **Check debug mode**: Look at "CSV Data Analysis" section
- **Verify location**: Ensure lat/lng coordinates are valid
- **Expand search**: Try larger radius or different acreage range
- **API limits**: Check if you've exceeded RapidAPI quotas

#### Authentication Problems
- **"Invalid key" error**: Verify `SECURE_KEY` in Vercel environment variables
- **Case sensitivity**: Environment variables are case-sensitive
- **Special characters**: Avoid spaces or special characters in keys

#### API Integration Issues
- **API call failed**: Check `RAPIDAPI_KEY` in environment variables
- **403/401 errors**: Verify your RapidAPI subscription is active
- **Rate limits**: Check if you've exceeded API call limits
- **Network issues**: Try again after a few minutes

### Vercel-Specific Troubleshooting

#### Deployment Issues
- **Build failures**: Check Vercel function logs
- **Environment variables**: Ensure they're set in Vercel dashboard
- **Cold starts**: First request may take 10-15 seconds

#### Performance
- **Function timeout**: Hobby plan has 10-second limit
- **Large datasets**: Consider reducing `max_comps` parameter
- **Memory limits**: Vercel hobby plan has memory restrictions

## 📞 Getting Help

### Self-Service Options
1. **Use Debug Mode**: Most issues can be diagnosed with the built-in debugging
2. **Check Logs**: Review Vercel function logs for detailed error messages
3. **Verify Setup**: Ensure all environment variables are correctly set

### External Resources
- **RapidAPI Support**: For API key or quota issues
- **Vercel Documentation**: For deployment and hosting questions
- **GitHub Issues**: Report bugs or request features in this repository

## 🔗 Related Services

- **RapidAPI PRYCD Comps**: [API Documentation](https://rapidapi.com/prycd/api/prycd-comps)
- **Vercel Platform**: [Deployment Guide](https://vercel.com/docs)
- **Flask Framework**: [Official Documentation](https://flask.palletsprojects.com/)
