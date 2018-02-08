import sys
from chemspipy import ChemSpider
import argparse
from PIL import Image
import requests
from io import BytesIO


def get_arguments():
    parser = argparse.ArgumentParser(description='SMILES molecule grid visualizer')
    parser.add_argument('-v', '--verbose', action='store_true', help="Display download status")
    parser.add_argument('--smiles', type=str, metavar='FILE', dest='smiles_file', default="./samples/smiles.txt", help='Grid of smiles strings (if not provided, sample file will be loaded)')
    parser.add_argument('--out', type=str, metavar='FILE', dest='image_file', default='neighborhood.jpg', help='Image of the smiles grid')
    parser.add_argument('--key', type=str, metavar='API_KEY', dest='api_key', help='ChemSpider API key (if not provided in apikey.txt file)')
    return parser.parse_args()


def stich_image(images, rows, cols):
    maxwidth = 0
    maxheight = 0
    for r in range(rows):
        for c in range(cols):
            maxwidth = max(maxwidth, images[r][c].size[0])
            maxheight = max(maxheight, images[r][c].size[1])

    final_width = maxwidth * cols
    final_height = maxheight * rows
    final_image = Image.new('L', (final_width, final_height))
    for r in range(rows):
        for c in range(cols):
            final_image.paste(images[r][c], (c * maxwidth, r * maxheight))
    return final_image


def download_images(chemspider, smiles_grid, rows, cols, verbose):
    images = [[]]
    for r in range(rows):
        for c in range(cols):
            if not r < len(images):
                images.append([])
            if verbose == True:
                sys.stdout.write('\rDownloading molecule image {} of {}'.format(r * cols + c + 1, rows * cols))
                sys.stdout.flush()
            apiqueryresult = chemspider.search(smiles_grid[r][c])
            url = apiqueryresult[0].image_url
            bytesimage = requests.get(url).content
            image = Image.open(BytesIO(bytesimage))
            images[r].append(image)
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

    final_image = stich_image(images, rows, cols)
    final_image.save(args.image_file)


if __name__ == "__main__":
    main()
