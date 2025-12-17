# Stress Testing Guide with Apache Bench

This guide explains how to stress test the Ethereum Wallet DeFi Score application using Apache Bench (ab).

## Prerequisites

1. **Install Apache Bench** (if not already installed):
   - **macOS**: Already included, or install via Homebrew: `brew install httpd`
   - **Linux**: `sudo apt-get install apache2-utils` (Ubuntu/Debian) or `sudo yum install httpd-tools` (CentOS/RHEL)
   - **Windows**: Download from Apache website or use WSL

2. **Ensure your Flask app is running** (for local testing):
   ```bash
   python app.py
   ```

## Understanding Apache Bench Parameters

- `-n`: Total number of requests to send
- `-c`: Number of concurrent requests (simultaneous connections)
- `-p`: Path to file containing POST data
- `-T`: Content-Type header for POST requests
- URL: The endpoint to test

## Stress Test Commands

### For Local Testing (localhost:5001)

```bash
# Start with low load
ab -n 10 -c 2 -p request.json -T application/json \
  http://localhost:5001/api/calculate

# Gradually increase
ab -n 50 -c 5 -p request.json -T application/json \
  http://localhost:5001/api/calculate

ab -n 100 -c 10 -p request.json -T application/json \
  http://localhost:5001/api/calculate

# Higher load
ab -n 200 -c 20 -p request.json -T application/json \
  http://localhost:5001/api/calculate

ab -n 500 -c 50 -p request.json -T application/json \
  http://localhost:5001/api/calculate

# Maximum stress test
ab -n 1000 -c 100 -p request.json -T application/json \
  http://localhost:5001/api/calculate
```

### For Production Deployment (docs.bitquery.io)

Replace the URL with your production endpoint:

```bash
# Start with low load
ab -n 10 -c 2 -p request.json -T application/json \
  https://docs.bitquery.io/ethereum-wallet-defi-score/api/calculate

# Gradually increase
ab -n 50 -c 5 -p request.json -T application/json \
  https://docs.bitquery.io/ethereum-wallet-defi-score/api/calculate

ab -n 100 -c 10 -p request.json -T application/json \
  https://docs.bitquery.io/ethereum-wallet-defi-score/api/calculate

# Higher load
ab -n 200 -c 20 -p request.json -T application/json \
  https://docs.bitquery.io/ethereum-wallet-defi-score/api/calculate

ab -n 500 -c 50 -p request.json -T application/json \
  https://docs.bitquery.io/ethereum-wallet-defi-score/api/calculate

# Maximum stress test
ab -n 1000 -c 100 -p request.json -T application/json \
  https://docs.bitquery.io/ethereum-wallet-defi-score/api/calculate
```

## Understanding the Results

Apache Bench will output metrics like:

- **Requests per second**: How many requests your server can handle
- **Time per request**: Average response time
- **Failed requests**: Number of requests that failed
- **Connection errors**: Network/connection issues
- **50th/90th/99th percentile**: Response time distribution

### Key Metrics to Watch:

1. **Requests per second**: Higher is better
2. **Failed requests**: Should be 0 (or very low)
3. **Time per request**: Lower is better (especially under load)
4. **Connection errors**: Should be 0

## Important Notes

⚠️ **Warning**: 
- Each request makes multiple API calls to Bitquery (P1, P2/P3, DEX/NFT, P4 queries)
- This will consume your Bitquery API quota quickly
- Consider using a test API key or monitoring your usage

⚠️ **Rate Limiting**:
- Bitquery API may have rate limits
- Your Flask app may need rate limiting to prevent abuse
- Consider implementing request throttling in production

## Tips

1. **Start small**: Always begin with low load (`-n 10 -c 2`) to ensure everything works
2. **Monitor your server**: Watch CPU, memory, and network usage during tests
3. **Check logs**: Monitor Flask application logs for errors
4. **Test incrementally**: Gradually increase load to find breaking points
5. **Test different addresses**: You can modify `request.json` with different addresses

## Example Output Interpretation

```
Requests per second:    45.23 [#/sec] (mean)
Time per request:       22.105 [ms] (mean)
Time per request:       11.052 [ms] (mean, across all concurrent requests)
Failed requests:        0
```

This shows:
- Server handles ~45 requests/second
- Average response time: 22ms
- No failures (good!)

## Troubleshooting

- **Connection refused**: Make sure your Flask app is running
- **SSL errors**: Use `http://` for local, `https://` for production
- **Timeout errors**: Your server may be overloaded, reduce `-c` (concurrency)
- **Failed requests**: Check server logs for errors

