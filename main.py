from tools.crawler import crawl_to_file
from tools.visualizer import visualize
from tools.worker import start_crawling
import sys
import yaml
from os import path, mkdir, getcwd
def is_int(val):
    try:
        int(val)
    except ValueError:
        return False
    return True

def load_config(file):
    with open("config/"+file, 'r') as stream:
        links = yaml.safe_load(stream)
        return links

if __name__ == "__main__":
    try:
        assert path.exists('config')
    except:
        print("Folder config not existed")
        mkdir(path.join(getcwd(), 'config'))
        print("config is created.\n")
    try:
        assert path.exists('data')
    except:
        print("Folder data not existed")
        mkdir(path.join(getcwd(), 'data'))
        print("data is created.\n")

    assert sys.argv[1] in ("crawl", "crawl_to_file", "visualize"), '"crawl" or "crawl_to_file" or "visualize" should be called'

    if sys.argv[1] == "crawl_to_file":
        assert sys.argv[2] in ("--input", "-I"), 'Should be "--input" or "-I".'
        assert sys.argv[3].endswith(('.yml', ".yaml")) , "File should be named by 'file_name.yml'."
        assert path.exists('config/{}'.format(sys.argv[3])), "File not existed"
        assert sys.argv[4] in ("--output", "-O"), 'Should be "--output" or "-0".'
        assert sys.argv[5].endswith(".json"), 'File should be named by "file_name.json".'
        links = load_config(sys.argv[3])
        assert links != None, f"No key in {sys.argv[3]}."
        for link in links:
            try:
                print(f"Crawling {link}: ")
                assert crawl_to_file(link, sys.argv[5]) == True, "\tlink is not valid or shopee has been shutdown\n"
            except AssertionError as msg:
                print(msg)
                continue

    elif sys.argv[1] == "visualize":
        assert sys.argv[2] in ("--file", "-F"), 'Should be "--file" or "-F".'
        assert sys.argv[3].endswith(".json"), 'File should be named by "file_name.json".'
        assert path.exists('data/{}'.format(sys.argv[3]))
        try:
            assert is_int(sys.argv[4]), "Number of product should be an integer.\n"
            length = int(sys.argv[4])
        except AssertionError as msg:
            print(msg)
            length=0
        except IndexError:
            length=1

        visualize(sys.argv[3], length)
    
    elif sys.argv[1] == "crawl":
        
        assert sys.argv[2] in ("--input", "-I"), 'Should be "--input" or "-I".'
        assert sys.argv[3].endswith(('.yml', ".yaml")) , "File should be named by 'file_name.yml'."
        try:
            assert is_int(sys.argv[4]), "Number of page should be an integer.\n"
            number_of_page=int(sys.argv[4])
        except AssertionError as msg:
            print(msg)
        except IndexError:
            number_of_page=1
        links = load_config(sys.argv[3])
        # start_crawling(links[0])
        print("Links in list:")
        for link in links:
            print(f"{link}")
        start_crawling(links, int(number_of_page))