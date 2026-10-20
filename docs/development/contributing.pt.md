# Contribuir com código

O guia geral é o [CONTRIBUTING](https://github.com/GTInfinityAscension/.github/blob/main/CONTRIBUTING.md) da GTInfinityAscension. A versão curta para o GTNA:

1. Para qualquer coisa maior que uma correção de bug, abra uma issue antes. Mudanças de balanceamento e progressão precisam da aprovação do autor.
2. Faça um fork, crie um branch a partir do `main`, um assunto por pull request.
3. Toda máquina, item ou receita nova vem com nomes em **en_us, pt_br e zh_cn**.
4. Acrescente ou atualize GameTests. Um multibloco novo precisa de um teste de formação e de um teste negativo (não pode formar nem rodar quando não deve).
5. Rode `./gradlew spotlessCheck compileJava runUnitTests runGameTestServer runData` e conte no pull request como testou no jogo.
6. Mensagens de commit e entradas do changelog são em inglês.
7. Ports mantêm o crédito da fonte: acrescente a máquina em `GTNASources` e siga as notas de licença do `THIRD_PARTY_NOTICES.md`.
