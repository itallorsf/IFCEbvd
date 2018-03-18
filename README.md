# IFSPbvd
### IFSP Biblioteca Virtual Downloader

Ferramenta de download de livros da biblioteca virtual do IFSP. Baixa página a página como imagem e depois converte para pdf. **É necessário uma matricula válida do IFSP e acesso ao sistema SUAP.**

### sintaxe:
**$ python ifspbvd.py [matricula] [senha] [id do livro]**

### Dependências
1. Biblioteca Selenium, para automatizar a interação com a página web.

2. Imagemagick, para juntar as imagens e montar o PDF (aqui você pode usar o que preferir).

3. Navegador Firefox (também pode usar o que preferir, apenas precisa modificar o caminho na linha 29).


Obs 1: na linha 27 o código comentado põe o Firefox em modo Headless (o navegador não é exibido) porém prefiro manter desativado essa função pois as vezes a internet oscila durante o download das páginas, voltar pra anterior ou atualizar a página faz com que o download continue normalmente depois.

Obs 2:  para mais informações veja a página do projeto original, eu apenas o modifiquei para funcionar no sistema do IFSP.

Obs 3: talvez para rodar no linux deva mudar a linha 110 para 
```  os.system('rm *.jpg')```
