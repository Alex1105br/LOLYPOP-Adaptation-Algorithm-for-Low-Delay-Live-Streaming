# Adaptive Video Streaming Player using Buffer-based (BB) Algorithm

Este projeto implementa um player de streaming de vídeo adaptativo que utiliza o Buffer-based (BB) Algorithm para ajustar a taxa de bits de vídeo com base no tamanho do buffer e nas condições da rede. O ambiente simula condições de rede usando traces (arquivos de rastreamento) para testar o desempenho do algoritmo em vários cenários.

## Estrutura do Projeto

![Overview do Projeto](/figs/overview.png)

- **bb.py**: Implementa o algoritmo Buffer-based (BB), que seleciona a taxa de bits do próximo chunk de vídeo com base no tamanho atual do buffer.
- **fixed_env.py**: Define o ambiente de simulação do streaming de vídeo. Este módulo simula o ambiente de rede e entrega chunks de vídeo de acordo com a largura de banda disponível e outras restrições.
- **load_trace.py**: Carrega os traces de rede, que são usados para simular diferentes condições de largura de banda na rede.
- **player.py**: Controla o fluxo do player de streaming de vídeo adaptativo, executa o BB Algorithm e registra o desempenho do algoritmo.
- **plot_logs.py**: Script para gerar gráficos de taxa de bits (bitrate) e tamanho do buffer ao longo do tempo, usando os dados de log gerados pelo `player.py`.
- **traces**: Pasta contendo arquivos de traces de rede para a simulação.
- **results**: Pasta onde os logs de execução são armazenados.
- **graphs**: Pasta onde os gráficos gerados pelo script de plotagem são armazenados.

## Estrutura dos Arquivos

- traces/: Contém os arquivos de trace de rede usados para a simulação.
- envivio/: Inclui arquivos de tamanhos de chunks de vídeo para cada nível de taxa de bits.
- results/: Logs de execução serão salvos nesta pasta.
- graphs/: Gráficos gerados pelo script de plotagem serão salvos nesta pasta.

## Configuração do Ambiente

### Pré-requisitos

Certifique-se de ter o Python 3.6 ou superior instalado. O projeto depende das seguintes bibliotecas:

- `numpy`
- `pandas`
- `matplotlib`

Instale as dependências com o seguinte comando:

```bash
pip install -r requirements.txt
```

## Execução

### 1. Executar o Player

Para rodar o player e simular o streaming de vídeo adaptativo com o BB Algorithm, execute o seguinte comando:

```bash
python player.py
```

O player.py inicializa o ambiente, executa o BB Algorithm para selecionar a taxa de bits e simula a transmissão de chunks de vídeo. Cada iteração registra informações sobre o atraso, tempo de rebuffering, tamanho do buffer, taxa de bits, etc.

Os resultados serão salvos na pasta results/ em arquivos de log individuais.

### 2. Gerar Gráficos dos Logs

Após executar o player e gerar os logs, você pode executar o script plot_logs.py para gerar gráficos de taxa de bits e tamanho do buffer ao longo do tempo.

Para executar o script de plotagem, use o seguinte comando:

```bash
python plot_logs.py
```

Este script lerá cada arquivo de log na pasta results/, gerará gráficos de bitrate e de tamanho do buffer ao longo do tempo e os salvará na pasta graphs/.


### Execução completa do docker

Executando com o docker, não é necessário executar nenhum outro comando. 
A instalação das dependências, execução do player e a geração dos gráficos será feita de forma sequencial.

```bash
docker-compose up 
```

### Exemplo de Log de Saída
Um exemplo de log no arquivo results/log_[nome_do_trace].txt:

```csv
time_stamp, bit_rate, buffer_size, rebuffer_time, chunk_size, download_time, throughput
0.0, 300, 12.5, 0.0, 1500000, 100.0, 2000.0
4.0, 750, 25.0, 0.0, 3000000, 150.0, 2500.0
...

```

<!-- ## Contribuições

Contribuições são bem-vindas! Se você tiver alguma ideia para melhorar o projeto, ou encontrar algum bug, sinta-se à vontade para abrir uma issue ou enviar um pull request. -->

<!-- ### Fork o repositório para sua conta GitHub.

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/adaptive-streaming-player.git
```

Crie uma branch para suas alterações:

```bash
git checkout -b minha-alteracao
```

Faça suas alterações e adicione commits descritivos.

Envie seu pull request e aguarde a revisão.
Licença
Distribuído sob a licença MIT. Consulte o arquivo LICENSE para mais informações.
 -->
