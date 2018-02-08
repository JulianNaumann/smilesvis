# Smiles visualizer

Use this tool to visualize a grid of smiles. This can be used to explore the latent space of a variational auto encoder like <https://github.com/JulianNaumann/grammarVAE>


## Requirements

Requires Python 3 and Chemspider to be installed. To install the chemspider library, do
```pip3 install chemspipy```


## ChemSpider API key

For access to the ChemSpider database (<https://www.chemspider.com>) you need to obtain your own API key from your profile page (<http://www.chemspider.com/UserProfile.aspx>) and put it into ```apikey.txt```.


## Usage
```
usage: smilesvis.py [-h] [-v] [--smiles FILE] [--out FILE] [--key API_KEY]

SMILES molecule grid visualizer

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Display download status
  --smiles FILE  Grid of smiles strings (if not provided, sample file will be loaded)
  --out FILE     Image of the smiles grid
  --key API_KEY  ChemSpider API key (if not provided in apikey.txt file)
```