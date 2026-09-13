import streamlit as st
from utils.file_utils import parse_uploaded_file
from utils.pipelines import generate_meeting_summary

st.set_page_config(page_title="Compte rendu automatique de réunion", layout="wide")

def run():
    if st.button("⬅️ Retour au catalogue"):
          del st.session_state['current_page']
          st.rerun()  # reviens sur le main
          
    st.title("🧭 Compte rendu automatique de réunion")

    uploaded_file = st.file_uploader("📄 Importer une transcription (.txt, .pdf, .docx)", type=["txt", "pdf", "docx"])
    manual_text = st.text_area("... ou collez directement le texte de la réunion :", height=200)

    if uploaded_file:
        text = parse_uploaded_file(uploaded_file)
    else:
        text = manual_text

    if st.button("Générer le compte rendu") and text:
        with st.spinner("Analyse en cours..."):
            report = generate_meeting_summary(text)

        st.success("✅ Compte rendu généré")

        # Résumé global
        st.subheader("📋 Synthèse générale")
        st.markdown(report["global_summary"])

        # Affichage sujet par sujet
        for topic in report["topics"]:
            with st.expander(f"📌 Sujet {topic['topic_id'] + 1}"):
                st.markdown(f"**Résumé :** {topic['summary']}")
                
                if topic.get("decisions"):
                    st.markdown("**✅ Décisions :**")
                    for d in topic["decisions"]:
                        st.markdown(f"- {d}")
                
                if topic.get("actions"):
                    st.markdown("**📅 Actions :**")
                    for a in topic["actions"]:
                        assignee = a.get("person", "—")
                        task = a.get("task", "")
                        due = a.get("due_date", "")
                        st.markdown(f"- **{assignee}** → {task} ({due})")
                
                if topic.get("kpi"):
                    st.markdown("**📊 Données / KPI :**")
                    st.dataframe(topic["kpi"])

        # Tableau global d'actions
        all_actions = [
            {**a, "Sujet": i + 1}
            for i, t in enumerate(report["topics"])
            for a in t.get("actions", [])
        ]
        if all_actions:
            st.subheader("🧾 Vue globale des actions")
            st.dataframe(all_actions)

    elif not text:
        st.info("💡 Importez ou collez une transcription pour démarrer.")
