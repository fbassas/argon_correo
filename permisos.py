import argparse
import imaplib

# explicacio de permisos a man cyradm
PERMISOS_ESCRIPTURA = 'lrswipkxtea'
PERMISOS_LECTURA = 'lrs'


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('usuari',help="Usuari")
  parser.add_argument('--ro',help="posar bustia usuari en read-only",action="store_true")
  parser.add_argument('--rw',help="posar bustia usuari en escriptura",action="store_true")
  arguments = parser.parse_args()

  connection = imaplib.IMAP4_SSL('imap-ct.upc.edu')
  connection.login('cyrusadm','vppcdjeD06')

  bustia = 'user/' + arguments.usuari 
  (resultat,llista_carpetes) = connection.list(bustia,'*')
  # La llista de carpetes es una llista de strings on cada un d'ells es
  #     < \HasChildren o \HasNoChildren > "/" "carpeta"
  #print llista_carpetes

  # separo el string utilitzant el " per si hi ha espais en blanc
  llista_final = [el.split('\"')[3] for el in llista_carpetes]
  #print llista_final

  for carpeta in llista_final:
    if arguments.ro:
      connection.setacl(carpeta,arguments.usuari,PERMISOS_LECTURA)
    if arguments.rw:
      connection.setacl(carpeta,arguments.usuari,PERMISOS_ESCRIPTURA)

    (resultat,llista_permisos) = connection.getacl(carpeta)
    # La llista de permisos conte un unic element que es un string
    # El format del string es "nom_bustia usuari1 permisos_usuari1 usuari2 permisos_usuari2 ..."
    permisos = llista_permisos[0]
    print permisos


# Tipica invocacio
if __name__ == '__main__':
  main()

