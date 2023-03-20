import * as crypto from "crypto-js";
import forge from 'node-forge';
import { Buffer } from 'buffer';

export class Crypter{
    // public static encrypt(value: string) {
    //     const encryptedMessage = crypto.AES.encrypt(value, import.meta.env.VITE_ENCRYPTION_KEY, {
    //         mode: crypto.mode.CBC,
    //         padding: crypto.pad.Pkcs7,
    //     });
    //     return encryptedMessage.toString();
    // }

    // public static decrypt(value: string) {
    //     const decryptedMessage = crypto.AES.decrypt(value, import.meta.env.VITE_ENCRYPTION_KEY, {
    //         mode: crypto.mode.CBC,
    //         padding: crypto.pad.Pkcs7,  
    //     });
    //     return decryptedMessage.toString(crypto.enc.Utf8);
    // }

    public static encrypt(message: string) {
        // Generate a random key and IV
        const key = crypto.lib.WordArray.random(32);
        const iv = crypto.lib.WordArray.random(16);

        // Encrypt the message using AES-256 encryption and the generated key and IV
        const encryptedMessage = crypto.AES.encrypt(message, key, { iv: iv, keySize: 256/32 }).toString();

        // Concatenate the key and IV with the encrypted message
        const encodedKey = crypto.enc.Base64.stringify(key);
        const encodedIV = crypto.enc.Base64.stringify(iv);
        const encryptedData = encodedIV + encodedKey + encryptedMessage;

        // Return the encrypted message with the concatenated key and IV
        return encryptedData;
    }

    public static decrypt(encryptedData: string) {
        // Extract the IV, key, and encrypted message from the concatenated string
        const iv = crypto.enc.Base64.parse(encryptedData.substr(0, 24));
        const key = crypto.enc.Base64.parse(encryptedData.substr(24, 44));
        const encryptedMessage = encryptedData.substring(68);

        // Decrypt the encrypted message using the provided key and IV
        const decryptedMessage = crypto.AES.decrypt(encryptedMessage, key, { iv: iv, keySize: 256/32 }).toString(crypto.enc.Utf8);

        // Return the decrypted message
        return decryptedMessage;

    }
}

