# 📄 OCR Information Extraction - How It Works

## Overview
The enhanced OCR service uses **Azure Document Intelligence** to extract comprehensive information from utility bills (water/electricity).

---

## 🎯 What Information Can Be Extracted?

### 1. **CIL (Customer ID)** 🔢
- **Format: 1071324-101 (7 digits - 3 digits)**
- Also supports: 7-10 digit numbers without dash
- Patterns recognized:
  - `CIL: 1071324-101`
  - `N° Client: 1071324-101`
  - `رقم العميل: 1071324-101`
  - `Client ID: 1071324-101`
  - Any standalone number matching format

### 2. **Customer Name** 👤
- Arabic or French names
- Patterns recognized:
  - `Nom: أحمد المرزوقي`
  - `الاسم: فاطمة الزهراء`
  - `Client: Mohamed Idrissi`

### 3. **Amount Due** 💰
- Payment amount in Moroccan Dirhams
- Patterns recognized:
  - `Montant à payer: 450.50 DH`
  - `المبلغ المستحق: 450.50 درهم`
  - `Total Due: 450.50 MAD`
  - Standalone amounts: `450.50 DH`

### 4. **Due Date** 📅
- Payment deadline
- Patterns recognized:
  - `Date limite: 15/12/2024`
  - `تاريخ الاستحقاق: 15/12/2024`
  - `Due Date: 15-12-2024`
  - Any date in format: `DD/MM/YYYY` or `DD-MM-YYYY`

### 5. **Service Type** ⚡💧
- Type of utility service
- Keywords recognized:
  - Water: `Eau`, `ماء`, `Water`
  - Electricity: `Électricité`, `كهرباء`, `Electricity`

### 6. **Consumption** 📊
- Current period usage
- Patterns recognized:
  - `Consommation: 150 m³` (water)
  - `الاستهلاك: 500 kWh` (electricity)
  - `Consumption: 150 كيلووات`

### 7. **Previous Balance** 💳
- Outstanding balance from previous bills
- Similar patterns to Amount Due

---

## 🔍 Extraction Methods

### Method 1: **Extract Full Bill Information**
```python
from services.ocr_service import extract_bill_information, format_extracted_info_arabic

# Extract all information
bill_info = extract_bill_information(image_bytes)

# Result structure:
{
    "cil": "1071324-101",
    "name": "أحمد المرزوقي",
    "amount_due": 450.50,
    "due_date": "15/12/2024",
    "bill_date": "01/12/2024",
    "service_type": "ماء",
    "previous_balance": 100.00,
    "consumption": 150.0,
    "raw_text": "...full extracted text..."
}

# Format for display in Arabic
formatted_text = format_extracted_info_arabic(bill_info)
```

### Method 2: **Extract CIL Only** (Quick Mode)
```python
from services.ocr_service import extract_cil_from_image

# Extract only CIL number
cil = extract_cil_from_image(image_bytes)
# Returns: "1071324-101"
```

---

## 🎨 UI Features

### In Streamlit Application:

1. **Upload Section**
   - Accepts: PNG, JPG, JPEG, PDF
   - Shows image preview
   - Toggle: "استخراج كامل المعلومات" (Extract full info)

2. **Extraction Button**
   - Full mode: "🔍 استخراج المعلومات من الفاتورة"
   - Quick mode: "🔍 استخراج رقم CIL فقط"

3. **Results Display**
   - Formatted Arabic output showing all extracted fields
   - Auto-injects CIL into chat for immediate agent processing
   - Warning if CIL not found

---

## 📋 Supported Bill Formats

### Moroccan Utility Bills (Example):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    LYDEC / RADEEMA / ONEE
    فاتورة المياه والكهرباء
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

N° Client: 1071324-101
الاسم: أحمد المرزوقي
العنوان: شارع الحسن الثاني، الدار البيضاء

Date: 01/12/2024
تاريخ الاستحقاق: 15/12/2024

Service: Eau / ماء
Consommation: 150 m³

Montant à payer: 450.50 DH
المبلغ المستحق: 450.50 درهم

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🔧 How It Works Technically

### Step 1: **Image Analysis**
- Uses Azure Document Intelligence `prebuilt-read` model
- Performs OCR on the uploaded image
- Extracts all text with high accuracy

### Step 2: **Pattern Matching**
- Uses **Regular Expressions (regex)** to find specific patterns
- Supports **bilingual** (Arabic + French) patterns
- Multiple pattern attempts for robustness

### Step 3: **Data Extraction**
For each field:
```python
# Example: Extract CIL
cil_patterns = [
    r'(?:CIL|N°\s*Client|رقم\s*العميل)\s*:?\s*(\d{7}-\d{3})',  # With label: 1071324-101
    r'\b(\d{7}-\d{3})\b'  # Fallback: standalone format
]

for pattern in cil_patterns:
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        extracted_info["cil"] = match.group(1)
        break
```

### Step 4: **Validation & Formatting**
- Validates extracted data types (e.g., converts amount to float)
- Formats output in Arabic for user display
- Handles missing fields gracefully

---

## 🎯 Agent Integration

Once information is extracted:

1. **CIL** → Automatically sent to AI agent
2. **Agent Response** → Uses `check_payment` and `check_maintenance` tools
3. **Full Context** → User sees both extracted info AND agent analysis

### Example Flow:
```
User uploads bill image
    ↓
OCR extracts: CIL=1071324-101, Amount=450 DH
    ↓
Displays: "تم استخراج المعلومات بنجاح"
    ↓
Auto-sends to agent: "رقم CIL الخاص بي هو: 1071324-101"
    ↓
Agent checks payment & maintenance
    ↓
Returns full analysis in Arabic
```

---

## 🚀 Usage Examples

### Example 1: Water Bill
```python
# User uploads water bill image
bill_info = extract_bill_information(image_bytes)

# Result:
{
    "cil": "1071324-101",
    "name": "أحمد المرزوقي",
    "amount_due": 120.50,
    "service_type": "ماء",
    "consumption": 150.0
}
```

### Example 2: Electricity Bill
```python
# User uploads electricity bill
bill_info = extract_bill_information(image_bytes)

# Result:
{
    "cil": "2083456-202",
    "name": "فاطمة الزهراء",
    "amount_due": 450.00,
    "service_type": "كهرباء",
    "consumption": 500.0
}
```

---

## ✅ Advantages

1. **Multilingual**: Supports Arabic and French
2. **Flexible**: Multiple pattern matching for robustness
3. **Comprehensive**: Extracts 8+ data points
4. **User-Friendly**: Formatted Arabic output
5. **Integrated**: Auto-triggers AI agent analysis
6. **Fast**: Option for quick CIL-only extraction

---

## 🔄 Future Enhancements

- [ ] Support for table extraction (detailed consumption history)
- [ ] Barcode/QR code reading
- [ ] Multiple bill comparison
- [ ] Auto-detection of bill provider (LYDEC, RADEEMA, ONEE)
- [ ] Confidence scores for extracted fields
- [ ] Support for handwritten notes

---

## 📝 Notes

- **Accuracy**: Depends on image quality and text clarity
- **Language**: Optimized for Moroccan Arabic and French
- **Format**: Works best with standard utility bill layouts
- **Fallback**: If specific patterns fail, provides raw text for manual review

---

Built with Azure Document Intelligence + Smart Pattern Matching! 🎉
