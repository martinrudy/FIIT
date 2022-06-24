import java.util.ArrayList;
import java.util.Arrays;

// Meno študenta: Martin Rudolf
public class HandleTxs {

    private UTXOPool utxoPoolcopy;
    private ArrayList<UTXO> UTXOused = new ArrayList<>();
    private ArrayList<Transaction> verifiedTxslist = new ArrayList<>();
    private ArrayList<Integer> utxoIndexes = new ArrayList<>();
    /**
     * Vytvorí verejný ledger, ktorého aktuálny UTXOPool (zbierka nevyčerpaných
     * transakčných výstupov) je {@code utxoPool}. Malo by to vytvoriť obchrannú kópiu
     * utxoPool pomocou konštruktora UTXOPool (UTXOPool uPool).
     */
    public HandleTxs(UTXOPool utxoPool) {
        utxoPoolcopy = new UTXOPool(utxoPool);
    }

    /**
     * @return aktuálny UTXO pool. 
     * Ak nenájde žiadny aktuálny UTXO pool, tak vráti prázdny (nie nulový) objekt {@code UTXOPool}.
     */
    public UTXOPool UTXOPoolGet() {
        return utxoPoolcopy;
    }

    /**
     * @return true, ak 
     * (1) sú všetky výstupy nárokované {@code tx} v aktuálnom UTXO pool, 
     * (2) podpisy na každom vstupe {@code tx} sú platné, 
     * (3) žiadne UTXO nie je nárokované viackrát, 
     * (4) všetky výstupné hodnoty {@code tx}s sú nezáporné a 
     * (5) súčet vstupných hodnôt {@code tx}s je väčší alebo rovný súčtu jej
     *     výstupných hodnôt; a false inak.
     */
    public boolean txIsValid(Transaction tx) {
        ArrayList<Transaction.Input> txInputs = tx.getInputs();
        ArrayList<Transaction.Output> txOutputs = tx.getOutputs();
        ArrayList<UTXO> utxoList = utxoPoolcopy.getAllUTXO();
        ArrayList<RSAKey> inAddresses = new ArrayList<>();
        double inValueSum = 0;
        double outValueSum = 0;
        boolean inputLegit = false;



        for (int i = 0; i < tx.numInputs(); i++) {
            Transaction.Input input = txInputs.get(i);
            for (UTXO ut:utxoList) {
                if(ut.getIndex() == input.outputIndex && Arrays.equals(ut.getTxHash(), input.prevTxHash)) {
                    double inValue = utxoPoolcopy.getTxOutput(ut).value;
                    RSAKey inAddress = utxoPoolcopy.getTxOutput(ut).address;
                    if(input.signature == null || !utxoPoolcopy.getTxOutput(ut).address.verifySignature(tx.getDataToSign(i), input.signature) || UTXOused.contains(ut)){
                        return false;
                    }
                    else{
                        inValueSum += inValue;
                        inAddresses.add(inAddress);
                        UTXOused.add(ut);
                        inputLegit = true;
                    }
                }
            };
        }
        if (inputLegit){
            for (int i = 0; i < tx.numOutputs(); i++) {
                Transaction.Output output = txOutputs.get(i);
                if (output.value < 0){
                    return false;
                }
                else {
                    outValueSum += output.value;
                    if (inAddresses.contains(output.address)) {
                        utxoIndexes.add(i);
                    }
                }
            }
        }

        if (inValueSum != 0 && outValueSum != 0 && inValueSum >= outValueSum){
            return true;
        }
        return false;
    }

    /**
     * Spracováva každú epochu prijímaním neusporiadaného radu navrhovaných
     * transakcií, kontroluje správnosť každej transakcie, vracia pole vzájomne 
     * platných prijatých transakcií a aktualizuje aktuálny UTXO pool podľa potreby.*/

    public Transaction[] handler(Transaction[] possibleTxs) {
        Transaction[] verifiedTxs = {};
        UTXOused.clear();
        verifiedTxslist.clear();
        for (Transaction tx:possibleTxs) {
            utxoIndexes.clear();
            if(txIsValid(tx)){
                verifiedTxslist.add(tx);
                if(!utxoIndexes.isEmpty()){
                    for (int i = 0; i < utxoIndexes.size(); i++) {
                        UTXO utxo = new UTXO(tx.getHash(), utxoIndexes.get(i));
                        utxoPoolcopy.addUTXO(utxo, tx.getOutput(utxoIndexes.get(i)));
                    }
                }
            }
        }
        for (UTXO ut: utxoPoolcopy.getAllUTXO()) {
            if (UTXOused.contains(ut)){
                utxoPoolcopy.removeUTXO(ut);
            }
        }
        verifiedTxs = verifiedTxslist.toArray(verifiedTxs);
        return verifiedTxs;
    }
}
