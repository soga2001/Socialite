export function AbbreviateNumber(val: Number | String) {
    try {
        const abbreviations = ['', 'K', 'M', 'B', 'T']; // Add more as needed
        const tier = Math.log10(Math.abs(Number(val))) / 3 | 0;
        
        if (tier === 0) return Number(val).toString();
        
        const suffix = abbreviations[tier];
        const scale = Math.pow(10, tier * 3);
        const scaledNumber = Number(val) / scale;
  
        return scaledNumber.toFixed(2) + suffix;
    } catch (error) {
        return 0
    }
}