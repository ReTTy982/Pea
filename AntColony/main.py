def better_config(file):
    folder = Path('Dane')
    file = folder / file
    with open(f"{file}", 'r') as f:
        t = int(f.readline().strip())
        l = []
        for i in range(t):
            l.append([])
        row = 0
        column = 0
        liczba = ""
        read = f.read()
        read = ' '.join(read.split())
        for i in read:
            if i == " " or i == "\n":
                l[row].append(int(liczba))
                liczba = ""
                column += 1
                if column == t:
                    column = 0
                    row += 1
            else:
                liczba += i
        return l

# Czytanie pliku ini

def get_ini():
    tsp = {}
    with open("config.ini", 'r') as f:
        files_nr = int(f.readline().strip())
        algorithms = f.readline().strip().split(" ")
        for i in range(files_nr):
            x = f.readline().strip().split(" ")
            tsp[x[0]] = x[1:7]

        #output = f.readline().strip()
        content = f.read()
        output = re.findall(r'#\w+',content)
        output = output[0]
        output = output[1:] + ".csv"

        

    return tsp, output,algorithms