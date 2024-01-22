# jami-cli
A command line app for encrypting/decrypting text with a password

## install
`pip install jami-cli`


## usage

- encrypt
```
❯ jami encrypt
Type in your text: hello world
Password: 123 (hidden)
Repeat for confirmation: 123 (hidden)
rK_w8vK82y7fr3-GLOgsTAABhqCAAAAAAGWtWEEdwP4sZlY1wTyD0NZqLAk5z0CkD-EHqS_77wF3IPt-jODfNfKiLEFenpXE5BybcVVCeKf2LOBFJhOJ-U4YaBoN
```

- decrypt
```
❯ jami decrypt
Type in your encrypted text: rK_w8vK82y7fr3-GLOgsTAABhqCAAAAAAGWtWEEdwP4sZlY1wTyD0NZqLAk5z0CkD-EHqS_77wF3IPt-jODfNfKiLEFenpXE5BybcVVCeKf2LOBFJhOJ-U4YaBoN
Password: 123 (hidden)
hello world
