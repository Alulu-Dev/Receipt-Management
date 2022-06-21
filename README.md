# receipt_management

### Team members name

Beken adugna
Eshtaol Girma
Mikiyas Daniel
Rediate Befekadu
Zekariyas Alemu

### Advisor name

Mr. Tewodros Wondifraw

---

Receipts are documents that function as acknowledgment that something of value has been transferred from one party to another. It is a headache for many trying to organize tens and hundreds of receipts received in a day, week or year. Especially for civil servants who buy stuff from their own pocket and do the math with the finance office by giving the receipts they received from the shop. If they lose the receipts then they won't be able to get their own money. Customers also can’t manage all those mini papers manually and when they sit for long their chance of fading is very high.
Through understanding the problem better, we observed the main problem in our country being that vendors use fake register machines to print out receipts and give it to customers like the real one. This means vendors own two register machines, this will make the government not get the right amount of vat and all the money will be for the vendors.
Also, for personal expense management our app will try to provide this feature. Previous apps gave a solution by just only giving the receipts a category. As receipts play a great role in financial management, but usually receipts are small pieces of paper which are not ideal to store and even if stored they are hard to do analyses and summary, this is where we want to provide a software solution. When we read the important information from a photo of receipt and format and insert it into a database and read the data not just scan. This gives the ability to do queries and individual access to each field as pdf files are not suitable to do analysis. Our software aims to give the ability to produce a summary of the transactions, business visited frequently and price comparison for products or services made at different times and places, and by using pattern recognition algorithms over consumer purchase history data it predicts future expenses like things that they will buy the next day or week.

- ● Solve customers’ problems of losing receipts and being unorganized by taking pictures, read data and inserting it on database for next use
- ● Lessen tax fraud by checking tin number and ticket number on database
- ● provide daily expense management system for free
- ● Provide where to purchase what information using pattern recognition algorithms over consumer purchase history
- ● Predicts future expenses and things that they will buy the next day or week.

## Tools used

- python - flask-restx
- Vs Code and it's extension(Live share) for collaborated coding
- GitHub for version control

## Setup procedure

### Requirements

- Python@3.0 +
- tesseract 4 +

### Run the app

To install all dependencies

```bash
pip install -r requirement.txt
```

To Start the app
export api/**init**.py

```bash
export FLASK_APP=API/__init__.py
```

```bash
./run.sh
```

or

```bash
flask run
```

## References

- pyimagesearch, https://pyimagesearch.com/2021/11/15/tesseract-page-segmentation-modes-psms-explained-how-to-improve-your-ocr-accuracy/

- Flask-restx, https://flask-restx.readthedocs.io/en/latest/

- YouTube - Tesseract OCR Training for New Fonts Language, https://www.youtube.com/watch?v=N5Y6gZgvryQ

- YouTube - [ Image To Text ] Train new Font with Tesseract in Google Colab (5x Faster), https://www.youtube.com/watch?v=V2chutR7RZo&t=724s

- towardsdatascience - https://towardsdatascience.com/predict-vs-predict-proba-scikit-learn-bdc45daa5972
