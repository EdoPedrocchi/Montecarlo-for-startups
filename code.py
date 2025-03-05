import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Funzione di simulazione Monte Carlo
def simulazione_monte_carlo(capitale_iniziale, entrate_iniziali, tasso_crescita, costi_fissi, anni_simulazione, num_simulazioni):
    risultati = []
    
    # Simulazioni Monte Carlo
    for _ in range(num_simulazioni):
        capitale = capitale_iniziale
        flusso_cassa_annuo = []
        
        for anno in range(anni_simulazione):
            crescita_entrate = np.random.normal(tasso_crescita, 0.1)  # Variabilità del tasso di crescita
            entrate_anno = entrate_iniziali * (1 + crescita_entrate) ** anno
            flusso_anno = entrate_anno - costi_fissi  # Flusso di cassa annuale
            
            capitale += flusso_anno  # Aggiorna il capitale
            flusso_cassa_annuo.append(capitale)  # Memorizza il flusso di cassa

            # Se il capitale esaurisce, interrompi la simulazione
            if capitale <= 0:
                break
        
        risultati.append(flusso_cassa_annuo)
    
    # Converti i risultati in un DataFrame per l'analisi
    risultati_df = pd.DataFrame(risultati)
    return risultati_df

# Funzione per visualizzare i risultati
def visualizza_risultati(risultati_df, anni_simulazione):
    # Visualizza la probabilità di successo (punto di pareggio)
    successi = (risultati_df.iloc[:, -1] > 0).sum() / len(risultati_df)
    
    # Grafico dei flussi di cassa
    plt.figure(figsize=(10, 6))
    plt.plot(risultati_df.T, color='lightblue', alpha=0.3)
    plt.title('Simulazione dei flussi di cassa nel tempo (Monte Carlo)', fontsize=14)
    plt.xlabel('Anno', fontsize=12)
    plt.ylabel('Capitale disponibile (€)', fontsize=12)
    plt.grid(True)
    st.pyplot(plt)

    # Mostra la probabilità di successo
    st.write(f"Probabilità di raggiungere il punto di pareggio (capitalizzazione positiva): {successi * 100:.2f}%")
    
# Interfaccia utente con Streamlit
def main():
    st.title('Analisi della Sostenibilità Finanziaria della Startup')
    st.sidebar.header('Input dei Dati')

    # Input dei parametri da parte dell'utente
    capitale_iniziale = st.sidebar.number_input('Capitale iniziale (€)', min_value=0, value=100000, step=1000)
    entrate_iniziali = st.sidebar.number_input('Entrate iniziali annuali (€)', min_value=0, value=50000, step=1000)
    tasso_crescita = st.sidebar.slider('Tasso di crescita annuale (%)', min_value=0.0, max_value=0.5, value=0.2, step=0.01)
    costi_fissi = st.sidebar.number_input('Costi fissi annuali (€)', min_value=0, value=30000, step=1000)
    anni_simulazione = st.sidebar.slider('Numero di anni per la simulazione', min_value=1, max_value=10, value=5)
    num_simulazioni = st.sidebar.number_input('Numero di simulazioni Monte Carlo', min_value=100, value=10000, step=100)

    # Esegui la simulazione quando l'utente preme il pulsante
    if st.sidebar.button('Esegui Simulazione'):
        risultati_df = simulazione_monte_carlo(capitale_iniziale, entrate_iniziali, tasso_crescita, costi_fissi, anni_simulazione, num_simulazioni)
        visualizza_risultati(risultati_df, anni_simulazione)

# Avvia il progetto Streamlit
if __name__ == '__main__':
    main()
