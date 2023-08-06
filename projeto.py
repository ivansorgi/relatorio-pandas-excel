import pandas as pd
import win32com.client as win32

#importar a base de dados
tabela_vendas = pd.read_excel('Vendas.xlsx')

#visualizar a base de dados
pd.set_option('display.max_columns', None)
print(tabela_vendas)

print('-' * 50)

#faturamento por loja
faturamento = tabela_vendas[['ID Loja', 'Valor Final']].groupby('ID Loja').sum()
print(faturamento)

print('-' * 50)

#quantidade de produtos vendidos por loja
vendasloja = tabela_vendas[['ID Loja', 'Quantidade' ]].groupby('ID Loja').sum()
print(vendasloja)

print('-' * 50)

#ticket médio por produto em cada loja
ticket_medio = (faturamento['Valor Final'] / vendasloja['Quantidade']).to_frame()
ticket_medio = ticket_medio.rename(columns={0: 'Ticket Médio'})
print(ticket_medio)

print('-' * 50)

#enviar um email com o relatório
outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = 'sorgiivan@gmail.com'
mail.Subject = 'Relatório de Vendas por Loja'
mail.HTMLBody = f'''
<p>Prezados,</p>

<p>Segue o Relatório de Vendas por cada Loja.</p>

<p>Faturamento:</p>
{faturamento.to_html(formatters={'Valor Final': 'R${:,.2f}'.format})}

<p>Quantidade Vendida:</p>
{vendasloja.to_html()}

<p>Ticket Médio dos Produtos em cada Loja:</p>
{ticket_medio.to_html(formatters={'Ticket Médio': 'R${:,.2f}'.format})}

<p>Qualquer dúvida estou à disposição.</p>

<p>Att.,</p>
<p>Ivan</p>
'''

mail.Send()

print("Email enviado!")

df = pd.DataFrame(faturamento)
tabela_html = df.to_html(formatters={'Valor Final': 'R${:,.2f}'.format})
print(tabela_html)

df1 = pd.DataFrame(vendasloja)
tabela_html1 = df1.to_html()
print(tabela_html1)

df2 = pd.DataFrame(ticket_medio)
tabela_html2 = df2.to_html(formatters={'Ticket Médio': 'R${:,.2f}'.format})
print(tabela_html2)