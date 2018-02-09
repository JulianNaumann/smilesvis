# Smiles visualizer

Use this tool to visualize a grid of smiles. This can be used to explore the latent space of a variational auto encoder like <https://github.com/JulianNaumann/grammarVAE>


## Requirements

Requires Python 3 and Chemspider to be installed. To install the chemspider library, do
```pip3 install chemspipy```


## ChemSpider API key

For access to the ChemSpider database (<https://www.chemspider.com>) you need to obtain your own API key from your profile page (<http://www.chemspider.com/UserProfile.aspx>) and put it into ```apikey.txt```.


## Use sample
To use the provided sample, type ```smilesvis.py ./samples/smiles.txt```


## Usage
```
usage: smilesvis.py [-h] [-v] [--key API_KEY] SMILESFILE

SMILES molecule grid visualizer

positional arguments:
  SMILESFILE     Grid of smiles strings

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Display download status
  --key API_KEY  ChemSpider API key (if not provided in apikey.txt file)```
