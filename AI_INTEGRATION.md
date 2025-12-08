# AI Integration Guide for Detective Joe

## Overview
Detective Joe now includes intelligent reconnaissance analysis powered by **Google Gemini 1.5 Flash**, a free, stable, and powerful AI model that provides:

- 🤖 **Intelligent Analysis**: Deep insights from reconnaissance data
- 🎯 **Risk Assessment**: Automated security risk scoring and classification
- 🔍 **Vulnerability Detection**: AI-powered identification of security issues
- 📊 **Attack Surface Analysis**: Comprehensive evaluation of exposed assets
- 💡 **Smart Recommendations**: Context-aware security guidance
- 📝 **Human-Readable Reports**: Professional summaries for stakeholders

## Getting Started

### 1. Install Dependencies

```bash
# Activate your virtual environment
source .venv/bin/activate

# Install the Gemini AI package
pip install google-generativeai
```

Or reinstall all requirements:
```bash
pip install -r requirements.txt
```

### 2. Get Your Free Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

**Note**: Gemini 1.5 Flash is **FREE** with generous rate limits and is the stable production-ready version!

### 3. Configure the API Key

You have three options:

#### Option A: Environment Variable (Recommended)
```bash
export GEMINI_API_KEY="your-api-key-here"
```

To make it permanent, add to your `~/.bashrc` or `~/.zshrc`:
```bash
echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

#### Option B: Configuration File
Edit `ai_config.yaml`:
```yaml
gemini:
  api_key: "your-api-key-here"
```

#### Option C: Pass at Runtime (Advanced)
```python
from gemini_service import GeminiService
gemini = GeminiService(api_key="your-api-key-here")
```

### 4. Test the Integration

```bash
# Run a simple scan to test AI features
python3 detectivejoe.py -c website -t example.com -p demo

# The report will include AI-powered analysis
```

## Features

### AI-Powered Analysis

When Gemini AI is enabled, Detective Joe provides:

1. **Intelligent Risk Scoring**
   - Context-aware risk assessment
   - Considers multiple factors simultaneously
   - Provides justification for risk levels

2. **Vulnerability Correlation**
   - Identifies relationships between findings
   - Suggests potential CVEs
   - Prioritizes by real-world impact

3. **Attack Surface Mapping**
   - Quantifies exposed assets
   - Identifies high-risk areas
   - Suggests surface reduction strategies

4. **Smart Recommendations**
   - Actionable security advice
   - Prioritized by urgency and impact
   - Specific remediation steps

5. **Executive Summaries**
   - Professional, stakeholder-ready reports
   - Technical details simplified
   - Clear next steps

### Fallback Mode

If Gemini AI is unavailable, Detective Joe automatically falls back to rule-based analysis:
- Basic risk scoring
- Pattern matching for vulnerabilities
- Standard recommendations
- Still functional, but less intelligent

## Usage Examples

### Basic Scan with AI
```bash
python3 detectivejoe.py -c website -t target.com
```

### Deep Analysis
```bash
python3 detectivejoe.py -c website -t target.com -p deep
```

### Multiple Targets
```bash
# Scan multiple targets
for target in site1.com site2.com site3.com; do
    python3 detectivejoe.py -c website -t $target
done
```

## Understanding AI Reports

### Risk Levels
- **CRITICAL** (80-100): Immediate action required
- **HIGH** (50-79): Significant vulnerabilities
- **MEDIUM** (25-49): Moderate concerns
- **LOW** (10-24): Minor issues
- **MINIMAL** (0-9): Good security posture

### Report Sections

1. **Executive Summary**: High-level overview
2. **Risk Assessment**: Detailed risk analysis
3. **Key Findings**: Most important discoveries
4. **Vulnerabilities**: Security issues identified
5. **Attack Surface**: Exposed assets analysis
6. **Attack Vectors**: Potential exploitation paths
7. **Recommendations**: Actionable security advice
8. **MITRE ATT&CK**: Mapped reconnaissance techniques

## Privacy & Security

### Data Handling
- Reconnaissance data is sent to Google Gemini API for analysis
- Google's data retention policies apply
- Consider sanitizing sensitive targets before scanning

### Best Practices
1. ✅ Use for authorized testing only
2. ✅ Review AI recommendations (they're suggestions)
3. ✅ Keep API keys secure
4. ✅ Monitor API usage
5. ❌ Don't share API keys
6. ❌ Don't scan without permission

### Sanitization
For sensitive targets, consider:
- Anonymizing target names in reports
- Using demo mode for testing
- Reviewing data before AI analysis

## Troubleshooting

### "Gemini AI not available"
```bash
# Check if package is installed
pip list | grep google-generativeai

# If not, install it
pip install google-generativeai
```

### "No API key found"
```bash
# Check environment variable
echo $GEMINI_API_KEY

# Set it if missing
export GEMINI_API_KEY="your-api-key"
```

### "API key invalid"
- Verify your key at [Google AI Studio](https://makersuite.google.com/app/apikey)
- Check for typos or extra spaces
- Generate a new key if needed

### "Rate limit exceeded"
- Free tier has limits (check Google's current limits)
- Wait a few minutes before trying again
- Consider spacing out scans

### "AI analysis failed"
- Detective Joe automatically falls back to rule-based analysis
- Check logs for specific error: `state/detective_joe.log`
- Ensure internet connectivity

## Advanced Configuration

### Custom AI Settings

Edit `ai_config.yaml`:

```yaml
gemini:
  # Adjust creativity vs consistency
  generation_config:
    temperature: 0.7  # Lower = more consistent, Higher = more creative
    max_output_tokens: 8192  # Maximum response length

ai_analysis:
  # Enable/disable features
  detailed_vulnerability_analysis: true
  attack_vector_identification: true
  mitre_attack_mapping: true
```

### Integration with Other Tools

Export results for use with other security tools:

```bash
# Generate all formats
python3 detectivejoe.py -c website -t example.com

# Reports are saved in multiple formats:
# - TXT: Human-readable
# - HTML: Interactive report
# - JSON: Machine-readable
# - CSV: Spreadsheet analysis
# - XML: SIEM integration
```

## Cost Information

### Free Tier (Gemini 1.5 Flash)
- **Model**: gemini-1.5-flash-latest
- **Cost**: FREE
- **Rate Limits**: Generous (60 RPM for free tier, check Google's current limits)
- **Perfect for**: Most reconnaissance needs
- **Status**: Stable, production-ready

### Paid Tiers (Optional)
- If you need higher limits, consider Google's paid plans
- Detective Joe works with any Gemini model
- Simply update the model name in `gemini_service.py`

## Examples of AI-Enhanced Reports

### Before (Rule-Based)
```
Risk Level: HIGH
Score: 65/100
Found 5 open ports, 3 services, 2 vulnerabilities
Recommendations: Standard security hardening
```

### After (Gemini AI)
```
Risk Level: HIGH
Score: 68/100

Executive Summary:
The target presents a HIGH-risk security posture due to multiple 
exposed services with known vulnerabilities. The outdated SSL/TLS 
configuration (SSLv3 enabled) exposes the system to POODLE attacks. 
Additionally, port 3389 (RDP) is publicly accessible without apparent 
IP restrictions, creating a significant attack vector.

Key Vulnerabilities:
1. [CRITICAL] SSLv3 enabled - Vulnerable to POODLE (CVE-2014-3566)
2. [HIGH] Remote Desktop (3389) exposed to internet
3. [MEDIUM] Outdated WordPress detected (version 5.2)

Immediate Actions Required:
1. Disable SSLv3, enable only TLS 1.2+
2. Restrict RDP access to trusted IPs
3. Update WordPress to latest version
4. Implement Web Application Firewall (WAF)
```

## Support & Contribution

- **Issues**: Report bugs on GitHub
- **Features**: Suggest improvements via issues
- **Documentation**: Help improve this guide
- **Code**: Submit pull requests

## Credits

- **Framework**: Detective Joe v1.5
- **AI Engine**: Google Gemini 1.5 Flash
- **Integration**: Open Source Community

---

**Remember**: AI is a powerful tool but not infallible. Always validate findings and use professional judgment when making security decisions.
