import streamlit as st
import json
import os

ARQUIVO_DADOS = "meu_financiamento.json"

# Funções de salvar/carregar (iguais ao anterior)
def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Configuração da página
st.set_page_config(page_title="Controle do Carro", page_icon="🚗", layout="centered")

# Título
st.title("🚗 Controle do Meu Financiamento")
st.markdown("---")

# Carrega os dados existentes
dados = carregar_dados()

# Se não tiver dados, pede para configurar
if dados is None:
    st.warning("⚠️ Nenhum financiamento cadastrado ainda. Configure abaixo:")
    
    with st.form("config_form"):
        valor_total = st.number_input("Valor total do carro financiado (R$)", min_value=0.0, step=1000.0)
        total_parcelas = st.number_input("Número TOTAL de parcelas do contrato", min_value=1, step=1)
        valor_parcela = st.number_input("Valor de cada parcela mensal (R$)", min_value=0.0, step=100.0)
        parcelas_pagas = st.number_input("Quantas parcelas você JÁ pagou até hoje?", min_value=0, step=1)
        
        if st.form_submit_button("💾 Salvar Dados"):
            dados = {
                "valor_total": valor_total,
                "total_parcelas": total_parcelas,
                "valor_parcela": valor_parcela,
                "parcelas_pagas": parcelas_pagas
            }
            salvar_dados(dados)
            st.success("✅ Dados salvos com sucesso!")
            st.rerun()

else:
    # Mostra o resumo
    pagas = dados["parcelas_pagas"]
    total = dados["total_parcelas"]
    faltam = total - pagas
    valor_pago = pagas * dados["valor_parcela"]
    valor_falta = faltam * dados["valor_parcela"]
    progresso = (pagas / total) * 100 if total > 0 else 0

    # Barra de progresso
    st.subheader("📊 Progresso do Pagamento")
    st.progress(progresso / 100)
    st.caption(f"{pagas} de {total} parcelas pagas ({progresso:.1f}%)")
    
    st.markdown("---")
    
    # Cards com informações
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Parcelas Pagas", f"{pagas}")
    with col2:
        st.metric("Faltam", f"{faltam}")
    with col3:
        st.metric("Total de Parcelas", f"{total}")
    
    col4, col5 = st.columns(2)
    with col4:
        st.metric("💰 Já Pago", formatar_moeda(valor_pago))
    with col5:
        st.metric("📉 Falta Pagar", formatar_moeda(valor_falta))
    
    st.markdown("---")
    
    # Botão para registrar pagamento
    st.subheader("💳 Registrar Pagamento")
    
    if pagas >= total:
        st.success("🎉 **PARABÉNS!** Seu carro está 100% pago! Você é livre!")
    else:
        qtd = st.number_input("Quantas parcelas você quer registrar como pagas?", 
                              min_value=1, max_value=faltam, value=1, step=1)
        
        if st.button("✅ Confirmar Pagamento", type="primary"):
            dados["parcelas_pagas"] += qtd
            salvar_dados(dados)
            st.success(f"✅ Registrado! Agora você pagou {dados['parcelas_pagas']} parcelas no total.")
            st.rerun()
    
    st.markdown("---")
    
    # Opções extras
    with st.expander("⚙️ Alterar dados do financiamento"):
        st.warning("Cuidado: isso vai sobrescrever os dados atuais!")
        novo_valor_total = st.number_input("Novo valor total", value=float(dados["valor_total"]))
        novo_total = st.number_input("Novo total de parcelas", value=int(dados["total_parcelas"]))
        novo_valor_parc = st.number_input("Novo valor da parcela", value=float(dados["valor_parcela"]))
        novo_pagas = st.number_input("Novo número de parcelas pagas", value=int(dados["parcelas_pagas"]))
        
        if st.button("💾 Salvar Alterações"):
            dados = {
                "valor_total": novo_valor_total,
                "total_parcelas": novo_total,
                "valor_parcela": novo_valor_parc,
                "parcelas_pagas": novo_pagas
            }
            salvar_dados(dados)
            st.success("✅ Alterado!")
            st.rerun()
