# Libre-RPG

Libre-RPG é um projeto open-source que nasceu da necessidade de mestres e jogadores de RPG terem acesso a um sistema gratuito e completo para sessões online e/ou presenciais. Embora a ideia não seja nova na comunidade, este projeto se diferencia por ser uma iniciativa criada para oferecer ferramentas de qualidade sem a barreira dos custos.

Nosso objetivo é fornecer um conjunto eficiente e acessível de ferramentas para qualquer pessoa, independentemente do uso, seja uma sessão casual entre amigos ou um programa de RPG transmitido ao vivo. O foco está em entregar uma experiência de qualidade, da forma como todo amante de RPG gostaria de ter.

## Roadmap

- [ ] Criação de múltiplas campanhas com conteúdos/membros diferentes
- [ ] Chat ao vivo para interação em tempo real
    - [ ] Rolagem de dados no chat (pública e privada)
    - [ ] Marcar jogadores no chat (gerar notificações)
- [ ] Visualização e edição de fichas de personagem
    - [ ] Visualização rápida do PDF da ficha
    - [ ] Exibição rápida de informações da ficha
    - [ ] 
- [ ] Visualizador de mapas da campanha
    - [ ] Visualização dinâmica do mapa da campanha
    - [ ] Movimentação de personagens no mapa (pelo mestre)
    - [ ] Cálculo de pontos de ação (no próprio mapa)
- [ ] Aba de configurações
    - [ ] Alterar preferências básicas do usuário
    - [ ] Ativar/Desativar animações e outros sistemas do tipo
- [ ] Compartilhamento de arquivos relacionados à campanha
    - [ ] Enviar/editar/remover arquivos
    - [ ] Escolher tipo de visualização dos arquivos (público ou pessoal)
- [ ] Soundboard controlada pelo mestre
    - [ ] Enviar/editar/efeitos sonoros arquivos
    - [ ] Mestre tocar efeitos sonoros para a mesa inteira
- [ ] Interface modular com prsonalização de abas e janelas
    - [ ] Reorganizar as abas da página principal
    - [ ] Redimensionamento das abas

## Tecnologias Utilizadas (até o momento)

- **Python**: Linguagem principal no back-end
- **Django**: Framework utilizado no modelo MVP
- **SQLite**: Banco de dados leve e portável

## Requisitos e Compatibilidade

O projeto foi desenvolvido para ser executado em qualquer sistema operacional, atendendo desde usuários avançados até os mais iniciantes.

- **Sistemas operacionais**: Linux, Windows, macOS
- **Acesso externo**: Para permitir conexões de fora da rede local, será necessário abrir uma porta no roteador ou utilizar ferramentas como Ngrok ou Radmin, além da possibilidade do acesso a port-forwarding pelo provedor de internet do mestre.

## Como Contribuir

Contribuições são muito bem-vindas! Por se tratar de um projeto de código aberto e gratuito, toda ajuda que agregue valor ao sistema é bem-vinda e valorizada. Quaiquer dúvidas podem ser feitas através da opção de issues aqui mesmo no repositório.

## Licença

Este projeto está licenciado sob os termos da licença MIT. Consulte o arquivo [LICENSE](./LICENSE.md) para mais informações.
