# SupplierSync
A Python tool for matching supplier product pricelists to an existing product database using exact and fuzzy matching techniques on Manufacturer Part Numbers (MPNs) and product names, optimized for accuracy and performance.
SupplierSync




SupplierSync is a Python script designed to match products from a supplier's pricelist to an existing product database. It uses a combination of exact matching on Manufacturer Part Numbers (MPNs) and fuzzy matching on MPNs and product names to ensure accurate product alignment. The script normalizes data to handle variations in formatting and outputs a CSV file with matching results, including match scores and types.

Features
Data Normalization: Cleans and standardizes MPNs and product names for consistent matching.
Exact Matching: Matches products using normalized MPNs for high-confidence results.
Fuzzy Matching: Uses rapidfuzz for flexible matching on MPNs and product names when exact matches fail.
Configurable: Easily adjust file paths, similarity thresholds, and required columns via a configuration dictionary.
Performance Tracking: Logs execution time and detailed match information for debugging and transparency.
Output: Saves results to a CSV file with supplier product details, matched IDs, match scores, and match types.
Requirements
Python 3.7 or higher
Required libraries:
pandas
rapidfuzz
Install dependencies using:
bash

Collapse

Wrap

Run

Copy
pip install pandas rapidfuzz
Installation
Clone the repository:
bash

Collapse

Wrap

Run

Copy
git clone https://github.com/your-username/SupplierSync.git
cd SupplierSync
Install the required Python libraries:
bash

Collapse

Wrap

Run

Copy
pip install -r requirements.txt
Usage
Prepare Input Files:
Existing Products CSV: A CSV file (Productsfile.csv) containing the existing product database with columns id, name, and MPN.
Supplier Pricelist CSV: A CSV file (products.csv) containing the supplier's products with at least id, name, and MPN columns.
Ensure both files are placed in the directory specified in the CONFIG dictionary (default: C:\Users\Salman\Desktop\WAREHOUSE\panga\).
Configure the Script:
Open Task1.py and update the CONFIG dictionary if needed:
existing_products_file: Path to the existing products CSV.
supplier_pricelist_file: Path to the supplier pricelist CSV.
output_file: Path where the matching results will be saved.
match_threshold: Similarity threshold for fuzzy matching (default: 90).
required_columns: Required columns for both input files (id, name, MPN).
Run the Script:
bash

Collapse

Wrap

Run

Copy
python Task1.py
The script will:
Load and validate the input CSV files.
Normalize MPNs and product names.
Perform exact and fuzzy matching.
Save results to the specified output CSV file (e.g., supplier_product_matched_results.csv).
Output:
The output CSV contains:
SupplierProductID: Supplier product ID.
SupplierProductName: Supplier product name.
SupplierMPN: Supplier MPN.
MatchedProductID: ID of the matched product in the existing database (if found).
MatchScore: Similarity score (0-100) for fuzzy matches.
MatchType: Type of match (Exact MPN, Fuzzy MPN, Fuzzy Name, or No Match).
Additional supplier columns (e.g., price, stock) prefixed with Supplier_.
Example
Input Files
Productsfile.csv (Existing Products):

csv

Collapse

Wrap

Copy
id,name,MPN
1,Apple iPhone 13,IPH13-128GB
2,Samsung Galaxy S21,SAM-GS21
products.csv (Supplier Pricelist):

csv

Collapse

Wrap

Copy
id,name,MPN,price
101,iPhone 13 128GB,IPH13-128-GB,999.99
102,Galaxy S21 5G,SAMGS21,799.99
Output File
supplier_product_matched_results.csv:

csv

Collapse

Wrap

Copy
SupplierProductID,SupplierProductName,SupplierMPN,MatchedProductID,MatchScore,MatchType,Supplier_price
101,iPhone 13 128GB,IPH13-128-GB,1,100,Exact MPN,999.99
102,Galaxy S21 5G,SAMGS21,2,100,Exact MPN,799.99
Configuration
The CONFIG dictionary in Task1.py allows customization:

python

Collapse

Wrap

Run

Copy
CONFIG = {
    'existing_products_file': r'C:\path\to\Productsfile.csv',
    'supplier_pricelist_file': r'C:\path\to\products.csv',
    'output_file': r'C:\path\to\supplier_product_matched_results.csv',
    'match_threshold': 90,  # Similarity threshold for fuzzy matching
    'required_columns': ['id', 'name', 'MPN'],
}
Notes
The script requires both input CSVs to have id, name, and MPN columns. Missing columns will raise an error.
Fuzzy matching uses the rapidfuzz library with a default similarity threshold of 90 (adjustable in CONFIG).
The script handles multiple MPN matches by logging them and skipping to avoid ambiguity.
Execution time is printed to monitor performance.
Contributing
Contributions are welcome! Please:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Commit your changes (git commit -m 'Add your feature').
Push to the branch (git push origin feature/your-feature).
Open a Pull Request.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Author
Salman Nawaz Malik
Steps to Add to GitHub
Create a New Repository:
Go to GitHub and create a new repository named SupplierSync.
Add the description: "A Python tool for matching supplier product pricelists to an existing product database using exact and fuzzy matching techniques on Manufacturer Part Numbers (MPNs) and product names, optimized for accuracy and performance."
Choose to initialize with a README (you can overwrite it later) and select the MIT License.
Prepare Your Local Repository:
Create a new directory for your project:
bash

Collapse

Wrap

Run

Copy
mkdir SupplierSync
cd SupplierSync
Copy Task1.py into this directory.
Create a requirements.txt file:
text

Collapse

Wrap

Copy
pandas
rapidfuzz
Create a README.md file and paste the content above.
(Optional) Create a LICENSE file with the MIT License text:
text

Collapse

Wrap

Copy
MIT License

Copyright (c) 2025 Salman Nawaz Malik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
Initialize and Push to GitHub:
Initialize a Git repository:
bash

Collapse

Wrap

Run

Copy
git init
git add Task1.py requirements.txt README.md LICENSE
git commit -m "Initial commit with SupplierSync script, README, and license"
Link to the GitHub repository:
bash

Collapse

Wrap

Run

Copy
git remote add origin https://github.com/your-username/SupplierSync.git
Push to GitHub:
bash

Collapse

Wrap

Run

Copy
git push -u origin main
Verify on GitHub:
Visit your repository on GitHub to ensure all files (Task1.py, requirements.txt, README.md, LICENSE) are uploaded.
The README will render automatically on the repository's main page.
Notes
Replace your-username with your actual GitHub username in the repository URL.
If your input CSV files (Productsfile.csv, products.csv) are not sensitive, you could include sample versions in the repository for testing, but avoid including real data.
The README is designed to be clear, professional, and informative, following GitHub best practices.
