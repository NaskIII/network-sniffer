# Network-Sniffer

Este script permite monitorar o tráfego de rede de uma máquina, exibindo informações sobre pacotes recebidos e enviados, dispositivos conectados à rede, e outros dados de rede relevantes. Ele pode ser usado para monitorar o tráfego de rede entre hosts específicos ou em toda a rede local.

## Funcionalidades:

- **Monitoramento de Pacotes**: Exibe o número de pacotes recebidos e enviados.
- **Dispositivos Conectados**: Exibe uma tabela com os dispositivos conectados à rede, incluindo o endereço IP e o endereço MAC.
- **Gráficos de Tráfego**: Exibe gráficos em tempo real com a quantidade de pacotes recebidos e enviados.
- **Últimos Pacotes**: Exibe informações sobre os últimos 10 pacotes capturados.
- **Controle de Usuário**: Permite sair do script pressionando a tecla "Tab".

## Requisitos:

- **Python 3.x**
- **Bibliotecas**:
  - `scapy`
  - `rich`
  - `asciichartpy`
  - `keyboard`
  
## Instalação das dependências:

O script requer a instalação de algumas bibliotecas. Elas podem ser instaladas utilizando um gerenciador de pacotes do Python, como o `pip`. 

```bash
pip install -r .\requirements.txt
```

### Instalação do Npcap

Se você estiver utilizando o Windows, o **Npcap** é necessário para a captura de pacotes. O Npcap fornece a interface de captura de pacotes de rede para o Scapy. 

1. Baixe o Npcap [aqui](https://npcap.com/#download).
2. Durante a instalação, certifique-se de selecionar a opção **"WinPcap API-compatible Mode"** para garantir que o Scapy consiga capturar pacotes.


## Como usar:

1. **Monitore toda a rede**:
   - O script monitora toda a rede local por padrão.

2. **Monitore tráfego entre dois hosts específicos**:
   - O script também pode ser configurado para monitorar o tráfego entre dois hosts específicos. Para isso, basta adicionar os endereços IP dos hosts diretamente no código.

3. **Controle de saída**:
   - Durante a execução do script, pressione a tecla `Tab` para sair do programa.

## Como funciona:

- O script captura pacotes de rede utilizando a biblioteca `scapy`.
- Utiliza ARP para descobrir dispositivos na rede e exibe uma tabela com os dispositivos conectados.
- Usa gráficos em tempo real para exibir o número de pacotes recebidos e enviados.
- Exibe as últimas 10 informações de pacotes capturados.

## Exemplo de Exibição:

- **Gráficos de Pacotes**: Gráficos em tempo real mostrando a quantidade de pacotes recebidos e enviados.
- **Tabela de Dispositivos**: Lista de dispositivos conectados à rede com IP e MAC.
- **Últimos Pacotes**: Exibe informações sobre os últimos 10 pacotes capturados, com origem e destino.

## Contribuindo:

Se você deseja contribuir para este projeto, basta realizar um fork deste repositório, fazer as alterações desejadas e abrir um pull request. Fique à vontade para adicionar novos recursos ou melhorar a documentação.

## Créditos

Esse software foi inspirado no repositório [Pynetmon](https://github.com/Sr-vZ/pynetmon/tree/main), apenas melhorei alguns aspectos do software e adicionei mais funcionalidades.
