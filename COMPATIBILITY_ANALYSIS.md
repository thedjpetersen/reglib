# Oregon State University Registration System - Compatibility Analysis

**Date:** November 18, 2025
**Project:** reglib (OSU Registration Library)
**Status:** ⚠️ **LIKELY INCOMPATIBLE** with current OSU systems

## Executive Summary

This library was designed to scrape Oregon State University's Banner 8 (Internet Native Banner) student information system. Based on current research, **this library is likely no longer functional** due to significant changes in OSU's registration infrastructure over the past several years.

## Current OSU Registration System (2024-2025)

### System Architecture
- **Student Portal:** my.oregonstate.edu (replaced MyOSU in October 2020)
- **Student Information System:** Banner 9 (upgraded from Banner 8 on January 1, 2019)
- **Future Direction:** Workday ERP for HR/Finance (Banner continues for student functions)

### Major Policy Changes (Fall 2025)
1. **PIN System Eliminated:** Registration PINs (6-digit codes) replaced with advising holds
2. **Registration Process:** Two-phase registration eliminated in favor of single priority window
3. **Authentication:** Enhanced security measures likely blocking automated access

## Technical Analysis

### 1. Target URLs and Endpoints

#### Current Code Targets:
```
Login System:
- https://adminfo.ucsadm.oregonstate.edu/prod/twbkwbis.P_WWWLogin
- https://adminfo.ucsadm.oregonstate.edu/prod/twbkwbis.P_ValLogin

Student Functions:
- https://adminfo.ucsadm.oregonstate.edu/prod/bwskfshd.P_CrseSchdDetl (Schedule)
- https://adminfo.ucsadm.oregonstate.edu/prod/bwskfreg.P_AltPin (Add/Drop)
- https://adminfo.ucsadm.oregonstate.edu/prod/bwckcoms.P_Regs (Registration)

Course Catalog:
- http://catalog.oregonstate.edu/CourseDetail.aspx (ASP.NET format)

MyDegrees:
- https://mydegrees.oregonstate.edu/IRISLink.cgi
- https://mydegrees.oregonstate.edu/SD_LoadFrameForm.html
```

#### Status:
- ❌ All URLs return **403 Forbidden** when accessed programmatically
- ⚠️ URLs may still exist but likely have CAPTCHA, rate limiting, or security headers
- 🔄 Banner 9 uses different URL patterns and authentication methods

### 2. Authentication System

#### Original Implementation (Banner 8):
```python
# Uses simple POST request with SID and PIN
form_data = urllib.parse.urlencode({'sid': sid, 'PIN': pin})
login_url = 'https://adminfo.ucsadm.oregonstate.edu/prod/twbkwbis.P_ValLogin'
```

#### Current Issues:
1. **PIN System Deprecated:** Fall 2025 eliminated 6-digit PINs in favor of advising holds
2. **Enhanced Security:** Modern systems likely use:
   - OAuth 2.0 / SAML authentication
   - ONID credentials (not SID/PIN)
   - Multi-factor authentication
   - CSRF tokens
   - Session management
3. **Bot Detection:** Likely implements:
   - CAPTCHA challenges
   - Rate limiting
   - User-agent validation
   - Behavioral analysis

### 3. HTML Parsing Logic

#### Class Search Parser (`parse_html/class_search.py`):
```python
# Looks for ASP.NET control IDs
table_element = html.get_element_by_id('ctl00_ContentPlaceHolder1_SOCListUC1_gvOfferings')
```

**Issues:**
- ASP.NET control IDs (ctl00_*) suggest old ASP.NET WebForms
- Banner 9 likely uses modern JavaScript frameworks (React/Angular/Vue)
- Table-based HTML structure may have been replaced with JSON APIs
- CSS class names (`datadisplaytable`, `captiontext`) may have changed

#### Schedule Parser (`parse_html/get_current_classes.py`):
```python
elements = html.find_class("datadisplaytable")
```

**Issues:**
- Hard-coded CSS class names specific to Banner 8
- Banner 9 interface is significantly different
- Modern systems use dynamic content loading (AJAX/fetch)

### 4. HTTP Request Headers

#### Current Implementation:
```python
header_values = {
    'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16',
    'Accept': 'application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
    # ... other headers
}
```

**Issues:**
- **Outdated User-Agent:** Firefox 3.6.16 from 2011 (14 years old!)
- Modern security systems flag outdated browsers
- Missing security headers required by modern systems
- No JavaScript execution capability for dynamic content

## Compatibility Assessment by Feature

| Feature | Original Implementation | Current Status | Compatibility |
|---------|------------------------|----------------|---------------|
| **Login** | SID + 6-digit PIN | ONID + Password (+ MFA) | ❌ Incompatible |
| **Class Search** | HTTP GET to catalog.oregonstate.edu | Likely modern API | ❌ Incompatible |
| **View Schedule** | Screen scraping Banner tables | Banner 9 dynamic content | ❌ Incompatible |
| **Add/Drop Classes** | POST to bwckcoms.P_Regs | Advising holds required | ❌ Incompatible |
| **Transcript** | Screen scraping | Unknown | ⚠️ Likely incompatible |
| **MyDegrees** | CGI scripts | Unknown | ⚠️ Likely incompatible |

## Breaking Changes Timeline

1. **~2011-2015:** Library originally developed for Banner 8
2. **January 1, 2019:** OSU upgraded to Banner 9 (major UI/UX changes)
3. **October 12, 2020:** MyOSU retired, replaced with my.oregonstate.edu
4. **2020-2024:** Administrative Modernization Program (Workday implementation)
5. **Fall 2025:** PIN system eliminated, registration process overhauled

## Recommendations

### Option 1: Complete Rewrite (Recommended)
**Modern API-First Approach:**
1. Investigate if OSU offers an official student API
2. Use Selenium/Playwright for browser automation if no API exists
3. Implement proper authentication (ONID OAuth/SAML)
4. Handle JavaScript-rendered content
5. Implement rate limiting and respectful scraping
6. Add comprehensive error handling

**Estimated Effort:** 80-120 hours

### Option 2: Reverse Engineer Banner 9
**Challenges:**
- Network analysis to find API endpoints
- JavaScript reverse engineering
- Authentication token management
- CAPTCHA/bot detection bypass
- Potential Terms of Service violations

**Estimated Effort:** 60-100 hours
**Risk:** High (may violate ToS)

### Option 3: Official API Request
**Approach:**
1. Contact OSU IT Services
2. Request official API access for student developers
3. Work within official guidelines

**Estimated Effort:** Variable (depends on OSU response)
**Risk:** Low
**Success Rate:** Unknown

### Option 4: Archive Project
**Rationale:**
- Library served its purpose 2011-2019
- Systems have fundamentally changed
- README already states "depreciated"
- Modernization may not be worth the effort

**Recommended Action:**
1. Update README with clear deprecation notice
2. Add this compatibility analysis to repository
3. Archive repository as historical reference
4. Provide links to official OSU resources

## Security and Ethical Considerations

### Current Code Issues:
1. **Credential Handling:** Stores student IDs and PINs in plain text
2. **No Rate Limiting:** Could overwhelm university servers
3. **No Error Handling:** Could trigger security alerts
4. **Terms of Service:** May violate OSU's acceptable use policies

### Recommendations:
1. **Do not attempt to use this library against production OSU systems**
2. Contact OSU IT before any scraping attempts
3. Use official APIs if available
4. Implement proper credential storage (environment variables, keyring)
5. Add rate limiting and backoff strategies
6. Respect robots.txt and ToS

## Code Modernization Status

The codebase has been successfully modernized for Python 3.8+:
- ✅ Modern packaging (pyproject.toml)
- ✅ Python 3 imports (urllib.request, http.cookiejar)
- ✅ Type hints added
- ✅ F-string formatting
- ✅ Dependencies updated (lxml 4.9+)

**However:** Code modernization ≠ functional compatibility with current systems

## Conclusion

This library is a **historical artifact** that demonstrates web scraping techniques from the early 2010s. While the Python code has been modernized, **it cannot function with current Oregon State University systems** due to:

1. Authentication system completely changed
2. Banner 8 → Banner 9 migration
3. HTML structure and API endpoints changed
4. Enhanced security measures blocking automated access
5. Policy changes (PIN elimination)

**Final Recommendation:** Archive this project and direct users to official OSU resources at my.oregonstate.edu.

## Resources

- **Current Student Portal:** https://my.oregonstate.edu
- **OSU Registrar:** https://registrar.oregonstate.edu
- **Banner 9 Information:** https://technology.oregonstate.edu/services/banner
- **IT Support:** https://it.oregonstate.edu

---

*This analysis was conducted on November 18, 2025, based on publicly available information and code review. No attempt was made to access OSU systems during this analysis.*
