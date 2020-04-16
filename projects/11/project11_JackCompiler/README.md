### Note:

This project was not made totally according to the guidelines. Although the api was partially implemented but the operation happens totally differently. Instead of picking each token one-by-one from tokenizer and then passing on to compilation engine based on the token's type etc. in the main function, the tokenizer tokenizes the whole file first and then the main only passes the whole list of tokens into commpilation engine. Rest of checks etc. happens inside the compilation engine. The parse tree then gets passed into the symbol table generator and then both the parse tree and symbol table gets passed into the code writer.

