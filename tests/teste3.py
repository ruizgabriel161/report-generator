def decode_cfemail(encoded_email):
    # O atributo "data-cfemail" contém o email codificado em hexadecimal.
    # Ele está na forma de "2 caracteres_hexadecimais 4 caracteres_hexadecimais ..."
    # Portanto, precisamos dividir a string em pares de caracteres.
    pairs = [encoded_email[i:i+2] for i in range(0, len(encoded_email), 2)]

    # Decodificando o email
    decoded_email = ""
    key = int(pairs[0], 16)
    for pair in pairs[1:]:
        decoded_email += chr(int(pair, 16) ^ key)

    return decoded_email

# Exemplo de uso:
encoded_email = "2e58474d5a415c6e4247585b5e004d4143004c5c"
decoded_email = decode_cfemail(encoded_email)
print(decoded_email)  # O email desofuscado será impresso aqui
