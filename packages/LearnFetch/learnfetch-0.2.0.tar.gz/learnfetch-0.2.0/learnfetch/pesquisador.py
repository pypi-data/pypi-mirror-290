import requests as req
from bs4 import BeautifulSoup as bs

class Pesquisador:
    """
    Classe Pesquisador para realizar buscas no site 'Toda Matéria' e extrair informações relevantes.

    Atributos:
        url (str): URL base para realizar buscas.
        domain (str): Domínio base do site 'Toda Matéria'.
        text (str): Texto acumulado das respostas das buscas.
        dados (list): Lista para armazenar os dados extraídos.

    Métodos:
        get_response(query: str) -> list:
            Realiza a busca no site 'Toda Matéria' usando a consulta fornecida e retorna os dados encontrados.
    """

    def __init__(self):
        """
        Inicializa uma instância da classe Pesquisador com a URL base e o domínio do site 'Toda Matéria'.
        """
        self.url = 'https://www.todamateria.com.br/?s='
        self.domain = 'https://www.todamateria.com.br'
        self.text = ''
        self.dados = []
        
    def get_response(self, query: str) -> list:
        """
        Realiza a busca no site 'Toda Matéria' usando a consulta fornecida.

        Args:
            query (str): Termo de busca a ser utilizado.

        Returns:
            list: Uma lista de dicionários contendo os dados extraídos dos resultados da busca.

        Exceções:
            Em caso de erro nas requisições HTTP ou ao acessar o conteúdo das páginas, mensagens de erro são impressas no console.
        """
        url = f'{self.url}{query}'
        res = req.get(url)
        
        if res.status_code == 200:
            print("Dados encontrados com sucesso!")
            soup = bs(res.content, 'html.parser')
            all_data = soup.find_all('a', class_='card-item')
            
            for data in all_data:
                try:  
                    link = data['href']
                    title = data['title']
                    urlpattern = f'{self.domain}{link}'
                    acessando = f'Acessando o link "{urlpattern}" ...'
                    print(acessando)
                    response = req.get(urlpattern)
                    
                    if response.status_code == 200:
                        acessado = 'Link acessado com sucesso!'
                        print(acessado)
                        try:
                            soup = bs(response.content, 'html.parser')
                            
                            content_wrapper = soup.find('div', class_='content-wrapper')
                            if content_wrapper:
                            
                                try:
                                    contents = content_wrapper.find_all('p')
                                    self.text += f'Pesquisar sobre: {title}\n {acessando} \n {acessado} \n \n'
                                    if contents:
                                        for content in contents:
                                            
                                            try:
                                                p = content.text.strip()
                                                self.text += p + '\n'
                                            except:
                                                print('Erro ao pegar o parágrafo novo!')
                                        self.dados.append({"title": title, "content": self.text}) 
                                        self.text = ''
                                    else:
                                        print('Nenhum parágrafo encontrado!')
                                except:
                                    print('Erro ao pegar o conteúdo!')
                            else:
                                print('Nenhum conteúdo encontrado!')    
                        except:
                            print('Erro ao acessar o conteúdo do artigo')
                except:
                    print('Erro ao obter o link:')
        else:
            print(f'Erro ao obter os dados: {res.status_code}')
        
        return self.dados

# Exemplo de uso
pqr = Pesquisador()
resultados = pqr.get_response("Fotossíntese")

print(resultados)
