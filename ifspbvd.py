# -*- coding: utf-8 -*-
#    _ ____       Instituto Federal de
#   (_) __/        Educação, Ciência e
#  / / _/          Tecnologia de São Paulo
# /_/_/  BIBLIOTECA VIRTUAL DOWNLOADER

from selenium import webdriver
import urllib, md5, os, sys
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait

def _baixa(_url,_nome):
  try:
    urllib.urlretrieve(_url, _nome)
  except:
    print 'Problemas ao baixar %s' % _nome
  else:
    print '%s baixado' % _nome

_hash = lambda(_mat): 'login=%s&token=%s' % (_mat, md5.new('%sQJEkJM2iLJiAj6LScxsZivml54SmzSy0' % _mat).hexdigest())

def _dump(matricula, senha, id_livro):
  options = Options()
  #options.add_argument('--headless')
  options.add_argument('--disable-gpu')
  driver = Firefox(executable_path='geckodriver', firefox_options=options) 
  b=driver
 
  try:
	  print 'Acessando o SUAP...'
	  b.get('https://suap.ifsp.edu.br/accounts/login/')
	
	  print 'SUAP acessado. \nFazendo login...'
	
	  b.find_element_by_id('id_username').send_keys(matricula)
	  b.find_element_by_id('id_password').send_keys(senha)
	  b.find_element_by_css_selector('body.login .submit-row input[type="submit"]').click()
	
	  b.implicitly_wait(2)
		
	  try:
		  b.find_element_by_class_name('errornote')
		  sys.exit("ERRO. Login ou senha inválidos!")
	  except:
		   print 'Login realizado com sucesso!'
  except Exception as e: print(e)
  
  print "Acessando biblioteca virtual..."
  try:
	  b.find_element_by_partial_link_text('Biblioteca Virtual Pearson').click()
	  print("Biblioteca acessada.")
  except Exception as e: print(e)
    
  print 'Gerando cookie de login para matricula %s...' % matricula
  b.get('http://ifsp.bv3.digitalpages.com.br/user_session/authentication_gateway?%s' % _hash(matricula))
  print 'Inicializando...'
  b.get('http://ifsp.bv3.digitalpages.com.br/users/publications/%s' % id_livro)
  print 'Obtendo informacoes para o livro %s...' % id_livro
  p_1 = 0
  while(p_1 == 0):
    try:
      p_1 = b.execute_script("if ($('.backgroundImg')[0]) { return 1 } else { return 0 }")
    except:
      p_1 = 0
  num_pag = int(b.execute_script("return RDP.options.pageSetLength")) - 2
  print 'preparando para baixar livro id=%s com %d paginas...' % (id_livro, num_pag)
  _baixa(b.execute_script("return $('.backgroundImg')[0].src"), "%s-00000.jpg" % id_livro)
  print 'baixando livro...'
  b.execute_script("navigate.next_page()")
  _v_p1, _v_p2 = '' , ''
  for i in range(1, num_pag, 2):
    # loop para esperar a pagina carregar
    p_1 , p_2 = 0 , 0
    while ((p_1==0) or (p_2==0)):
      try:
        p_1 = b.execute_script("if ($('.backgroundImg')[0]) { return 1 } else { return 0 }")
        p_2 = b.execute_script("if ($('.backgroundImg')[1]) { return 1 } else { return 0 }")
      except:
        p_1 , p_2 = 0 , 0
    # carregou, pegar endereco
    _p1 = b.execute_script("return $('.backgroundImg')[0].src")
    _p2 = b.execute_script("return $('.backgroundImg')[1].src")
    # checa se ainda não carregou a nova pagina
    while((_p1 == _v_p1) or (_p2 == _v_p2)):
      try:
        _p1 = b.execute_script("return $('.backgroundImg')[0].src")
        _p2 = b.execute_script("return $('.backgroundImg')[1].src")
      except:
        pass
    # carregou nova, baixar...
    _baixa(_p1, "%s-%05d.jpg" % (id_livro, i))
    _baixa(_p2, "%s-%05d.jpg" % (id_livro, i+1))
    # ajusta os novos valores
    _v_p1 , _v_p2 = _p1 , _p2
    b.execute_script("navigate.next_page()")
    print 'baixadas %d/%d paginas...' % (i,num_pag)
  print 'fim do dump'
  b.quit()

def _gerapdf(_livro):
  # usando a ferramenta convert do ImageMagick
  print 'Convertendo para PDF...'
  os.system('convert *.jpg %s.pdf' % _livro)

def _remove():
  print 'Limpando os jpgs residuais...'
  os.system('del *.jpg')

if __name__ == "__main__":
  if len(sys.argv) != 4:
    print "IFSP Biblioteca Virtual Pearson Downloader"
    print "Sintaxe: ./ifspbvd.py [matricula] [senha] [id do livro]"
    sys.exit(1)
  else:
    print "Iniciando... aguarde..."
    matricula = sys.argv[1]
    senha = sys.argv[2]
    livro = sys.argv[3]
    _dump(matricula, senha, livro)
    _gerapdf(livro)
    _remove()
    print '\033[92mFinalizado. Livro convertido em PDF com sucesso!. Ate mais! :) \033[0m'
