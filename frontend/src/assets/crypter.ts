import * as crypto from "crypto-js";

export class Crypter{
    public static encrypt(value: any) {
        const encryptedMessage = crypto.AES.encrypt(value, import.meta.env.VITE_ENCRYPTION_KEY, {
            mode: crypto.mode.CBC,
            padding: crypto.pad.Pkcs7,
        });
        return encryptedMessage.toString();
    }

    public static decrypt(value: string) {
        const decryptedMessage = crypto.AES.decrypt(value, import.meta.env.VITE_ENCRYPTION_KEY, {
            mode: crypto.mode.CBC,
            padding: crypto.pad.Pkcs7,  
        });
        return decryptedMessage.toString(crypto.enc.Utf8);
    }
}