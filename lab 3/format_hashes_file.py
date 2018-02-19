if __name__ == '__main__':
    f = open("hashes.txt",'r')
    f_out = open('formatted_hashes.txt','w')
    lines = f.readlines()
    lines = [line.replace('\n','') for line in lines]
    for line in lines:
        line = line.split(' ')
        if len(line) == 2:
            hashh = line[1]
            f_out.write(hashh+'\n') 
    f_out.close()
