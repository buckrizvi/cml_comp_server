# CML Comp Server - Vercel Deployment

A Flask web application for fetching comparable property data via RapidAPI, optimized for deployment on Vercel.

## Features

- Web form interface for property search parameters
- Integration with RapidAPI for property comparables
- CSV export functionality
- Secure key-based access
- Serverless deployment ready

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

## Vercel Deployment

### Prerequisites
- Vercel account (hobby plan supported)
- Vercel CLI installed: `npm install -g vercel`

### Deployment Steps

1. **Login to Vercel:**
   ```bash
   vercel login
   ```

2. **Deploy the project:**
   ```bash
   vercel
   ```
   - Follow the prompts to link/create a new project
   - Choose "y" when asked to link to existing project or create new
   - Accept default settings

3. **Set Environment Variables:**
   After deployment, set your environment variables in the Vercel dashboard:
   - Go to your project dashboard on vercel.com
   - Navigate to Settings > Environment Variables
   - Add:
     - `RAPIDAPI_KEY`: Your RapidAPI key
     - `SECURE_KEY`: Your chosen secure access key

4. **Redeploy to apply environment variables:**
   ```bash
   vercel --prod
   ```

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

## Usage

1. Navigate to your deployed Vercel URL
2. Enter your secure key
3. Fill in property search parameters:
   - Latitude/Longitude coordinates
   - Minimum/Maximum acreage
   - Search radius in miles
   - Maximum number of comparables
   - Comp age in days
   - Option to remove duplicates
4. Click "Get Comps" to download CSV results

## Environment Variables

- `RAPIDAPI_KEY`: Required. Your RapidAPI key for accessing the property comparables API
- `SECURE_KEY`: Required. A secret key to protect access to your application

## API Integration

This application integrates with the RapidAPI property comparables service:
- Endpoint: `https://prycd-comps.p.rapidapi.com/compsByLatLong`
- Returns property data in JSON format
- Exports results as CSV file

## Troubleshooting

### Common Issues

1. **"Invalid key" error**: Check that your `SECURE_KEY` environment variable matches what you're entering
2. **API call failed**: Verify your `RAPIDAPI_KEY` is valid and you have credits remaining
3. **Template not found**: Ensure the templates directory structure is correct

### Vercel-Specific Issues

1. **Function timeout**: Vercel hobby plan has 10-second function timeout
2. **Cold starts**: First request may be slower due to serverless cold start
3. **Logs**: Check function logs in Vercel dashboard for debugging

## Support

For issues with:
- Vercel deployment: Check Vercel documentation
- RapidAPI integration: Verify your API key and endpoint access
- Application bugs: Check the logs and error messages
