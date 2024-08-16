from agentfud_password_manager.utils import encrypt, decrypt, get_master_key

def test_encrypt_decrypt():
    master_key = get_master_key('Bla Bla Secret', 'laksE523')
    plaintext = "Sed ut perspiciatis unde omnis iste natus"
    ciphertext = encrypt(plaintext, master_key)
    assert decrypt(ciphertext, master_key) == plaintext