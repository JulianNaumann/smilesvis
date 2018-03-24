import sys
from chemspipy import ChemSpider
import argparse
from PIL import Image
import requests
from io import BytesIO


def get_arguments():
    parser = argparse.ArgumentParser(description='SMILES molecule grid visualizer')
    parser.add_argument('smiles_file', type=str, metavar='SMILESFILE', help='Grid of smiles strings')
    parser.add_argument('-v', '--verbose', action='store_true', help="Display download status")
    parser.add_argument('--key', type=str, metavar='API_KEY', dest='api_key', help='ChemSpider API key (if not provided in apikey.txt file)')
    return parser.parse_args()


def stich_image(images, rows, cols):
    maxwidth = 0
    maxheight = 0
    for r in range(rows):
        for c in range(cols):
            if images[r][c] == '':
                continue
            maxwidth = max(maxwidth, images[r][c].size[0])
            maxheight = max(maxheight, images[r][c].size[1])

    final_width = maxwidth * cols
    final_height = maxheight * rows
    final_image = Image.new('L', (final_width, final_height))
    for r in range(rows):
        for c in range(cols):
            if images[r][c] != '':
                final_image.paste(images[r][c], (c * maxwidth, r * maxheight))
    return final_image


def download_images(chemspider, smiles_grid, rows, cols, verbose):
    images = [[]]
    previousQueryResults = {}
    for r in range(rows):
        for c in range(cols):
            if verbose == True:
                sys.stdout.write('\rDownloading molecule image {} of {}'.format(r * cols + c + 1, rows * cols))
                sys.stdout.flush()
                
            if previousQueryResults.get(smiles_grid[r][c]) is None:
                apiqueryresult = chemspider.search(smiles_grid[r][c])
                if len(apiqueryresult) == 0:
                    image = ''
                else:
                    url = apiqueryresult[0].image_url
                    bytesimage = requests.get(url).content
                    image = Image.open(BytesIO(bytesimage))
                previousQueryResults[smiles_grid[r][c]] = image
            else:
                image = previousQueryResults.get(smiles_grid[r][c])                
            images[r].append(image)
        if r < rows - 1:
            images.append([])
    if verbose == True:
        sys.stdout.write('\n')
    return images


def getChemSpiderObject(api_key):
    if api_key is None:
        with open('apikey.txt', 'r') as api_file:
            api_key = api_file.readline().strip()
    return ChemSpider(api_key)

def main():
    args = get_arguments()
    chemSpiderObject = getChemSpiderObject(args.api_key)

    with open(args.smiles_file, "r") as f:
        smiles_grid = [[smile for smile in line.split()] for line in f.readlines()]

    rows = len(smiles_grid)
    cols = len(smiles_grid[0])
    images = download_images(chemSpiderObject, smiles_grid, rows, cols, args.verbose)

    filename = 'images/' + args.smiles_file.strip('.txt').split('/')[-1] + '.jpg'
    final_image = stich_image(images, rows, cols)
    final_image.save(filename)


if __name__ == "__main__":
    main()
