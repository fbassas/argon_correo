import sys,re
import os
import argparse

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('fitxers',nargs='*',help="Fitxers de log a mirar")
  arguments = parser.parse_args()

  for fitxer in arguments.fitxers:
    # format del nom
    #    francesc.bassas@upc.edu_09062020-1139.Leam.log

    with open(fitxer) as fd:
      nom_fitxer = os.path.basename(fitxer)
      # format del nom
      #    francesc.bassas@upc.edu_09062020-1139.Leam.log
      lis = nom_fitxer.split('_')
      correu = lis[0]
      # lis[1] similar a 09062020-1139.Leam.log
      lis2 = lis[1].split('.')
      carpeta = lis2[1]
      #print "correu: {0} carpeta: {1}\n".format(correu,carpeta)
      num_enviats = 0
      bytes_enviats = 0
      num_unable = 0
 
      for linia in fd:
        #print linia
        #
        # 11:39:59]: Connected to Gmail IMAP
        # [11:40:24]: Sending "Usuari de LEAM" (7919 bytes)
        # [11:40:31]: Skipping "cyrus.squat" - corrupted
        #
        #trobat = match = re.search(r'\s+(\d+)\s+(\d+)\s+\d+\.*',linia)
        trobat = re.search(r'\[[0-9:]+\]:\s+(\w+)\s+(.*)',linia)
        if trobat:
          # trobat.group(1) pot ser Connected,Sending,Skipping,...
          #print trobat.group(1)
          if trobat.group(1) == 'Sending':
            num_enviats += 1
            info_enviada = re.search(r'\".*\"\s\((\d+)\sbytes\)',trobat.group(2))
            if info_enviada:
              #print info_enviada.group(1)
              bytes_enviats += int(info_enviada.group(1))
            else:
              print "Error: no he trobat la info del Sending a {0}\n".format(trobat.group(2))
          elif trobat.group(1) == 'Unable':
            num_unable +=1
            # No es sending
            print "Error:  {0}\n".format(linia)
      print "correu: {0} carpeta: {1} enviats: {2} bytes: {3}\n".format(correu,carpeta,num_enviats,bytes_enviats)








if __name__ == '__main__':
    main()

