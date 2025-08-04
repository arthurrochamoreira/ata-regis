from datetime import date
from typing import List

# Importação absoluta para permitir execução direta ou como módulo
from models.ata import Ata

class EmailService:
    """Serviço para envio de emails (simulado com print)"""
    
    def __init__(self):
        self.destinatarios_padrao = [
            "diatu@trf1.jus.br",
            "seae1@trf1.jus.br"
        ]
    
    def enviar_alerta_vencimento(self, ata: Ata, destinatarios: List[str] = None) -> bool:
        """Envia alerta de vencimento de ata (simulado com print)"""
        if destinatarios is None:
            destinatarios = self.destinatarios_padrao
        
        try:
            print(f"\n{'='*50}")
            print("SIMULAÇÃO DE ENVIO DE EMAIL")
            print(f"{'='*50}")
            print(f"Para: {', '.join(destinatarios)}")
            print(f"Assunto: Ata {ata.numero_ata} próxima do vencimento")
            print(f"Data/Hora: {date.today().strftime('%d/%m/%Y')}")
            print(f"\nMensagem:")
            print(f"A Ata de Registro de Preços {ata.numero_ata} está próxima do vencimento.")
            print(f"\nDetalhes da Ata:")
            print(f"- Número: {ata.numero_ata}")
            print(f"- SEI: {ata.documento_sei}")
            print(f"- Objeto: {ata.objeto}")
            print(f"- Fornecedor: {ata.fornecedor}")
            print(f"- Data de Vencimento: {ata.data_vigencia.strftime('%d/%m/%Y')}")
            print(f"- Dias Restantes: {ata.dias_restantes}")
            print(f"- Status: {ata.status.replace('_', ' ').title()}")
            print(f"\nValor Total da Ata: R$ {ata.valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            
            print(f"\nItens da Ata:")
            for i, item in enumerate(ata.itens, 1):
                valor_formatado = f"R$ {item.valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                valor_total_formatado = f"R$ {item.valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                print(f"{i}. {item.descricao}")
                print(f"   Quantidade: {item.quantidade}")
                print(f"   Valor Unitário: {valor_formatado}")
                print(f"   Valor Total: {valor_total_formatado}")
            
            print(f"\nContatos do Fornecedor:")
            if ata.telefones_fornecedor:
                print(f"Telefones: {', '.join(ata.telefones_fornecedor)}")
            if ata.emails_fornecedor:
                print(f"E-mails: {', '.join(ata.emails_fornecedor)}")
            
            print(f"\nEste é um alerta automático do Sistema de Atas de Registro de Preços.")
            print(f"Por favor, tome as providências necessárias.")
            print(f"{'='*50}\n")
            
            return True
            
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            return False
    
    def enviar_alerta_multiplas_atas(self, atas: List[Ata], destinatarios: List[str] = None) -> bool:
        """Envia alerta para múltiplas atas próximas do vencimento"""
        if destinatarios is None:
            destinatarios = self.destinatarios_padrao
        
        if not atas:
            return False
        
        try:
            print(f"\n{'='*50}")
            print("SIMULAÇÃO DE ENVIO DE EMAIL - MÚLTIPLAS ATAS")
            print(f"{'='*50}")
            print(f"Para: {', '.join(destinatarios)}")
            print(f"Assunto: {len(atas)} atas próximas do vencimento")
            print(f"Data/Hora: {date.today().strftime('%d/%m/%Y')}")
            print(f"\nMensagem:")
            print(f"Existem {len(atas)} atas próximas do vencimento que requerem atenção:")
            
            for i, ata in enumerate(atas, 1):
                print(f"\n{i}. Ata {ata.numero_ata}")
                print(f"   Objeto: {ata.objeto}")
                print(f"   Fornecedor: {ata.fornecedor}")
                print(f"   Vencimento: {ata.data_vigencia.strftime('%d/%m/%Y')}")
                print(f"   Dias Restantes: {ata.dias_restantes}")
                
                if ata.dias_restantes <= 30:
                    print(f"   ⚠️ ATENÇÃO: Vencimento em menos de 30 dias!")
                elif ata.dias_restantes <= 7:
                    print(f"   🚨 URGENTE: Vencimento em menos de 7 dias!")
            
            print(f"\nEste é um alerta automático do Sistema de Atas de Registro de Preços.")
            print(f"Por favor, tome as providências necessárias para cada ata listada.")
            print(f"{'='*50}\n")
            
            return True
            
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            return False
    
    def enviar_relatorio_semanal(self, atas_vigentes: int, atas_a_vencer: int, atas_vencidas: int, 
                                atas_proximas: List[Ata], destinatarios: List[str] = None) -> bool:
        """Envia relatório semanal do status das atas"""
        if destinatarios is None:
            destinatarios = self.destinatarios_padrao
        
        try:
            print(f"\n{'='*50}")
            print("SIMULAÇÃO DE ENVIO DE EMAIL - RELATÓRIO SEMANAL")
            print(f"{'='*50}")
            print(f"Para: {', '.join(destinatarios)}")
            print(f"Assunto: Relatório Semanal - Atas de Registro de Preços")
            print(f"Data/Hora: {date.today().strftime('%d/%m/%Y')}")
            print(f"\nRelatório Semanal - Status das Atas:")
            
            total_atas = atas_vigentes + atas_a_vencer + atas_vencidas
            print(f"\nResumo Geral:")
            print(f"- Total de Atas: {total_atas}")
            print(f"- Vigentes: {atas_vigentes} ({(atas_vigentes/total_atas*100):.1f}%)" if total_atas > 0 else "- Vigentes: 0")
            print(f"- A Vencer (≤90 dias): {atas_a_vencer} ({(atas_a_vencer/total_atas*100):.1f}%)" if total_atas > 0 else "- A Vencer: 0")
            print(f"- Vencidas: {atas_vencidas} ({(atas_vencidas/total_atas*100):.1f}%)" if total_atas > 0 else "- Vencidas: 0")
            
            if atas_proximas:
                print(f"\nAtas que requerem atenção especial:")
                for ata in atas_proximas[:10]:  # Limita a 10 atas
                    print(f"- {ata.numero_ata}: {ata.objeto} (vence em {ata.dias_restantes} dias)")
                
                if len(atas_proximas) > 10:
                    print(f"... e mais {len(atas_proximas) - 10} atas")
            
            print(f"\nEste relatório é gerado automaticamente pelo Sistema de Atas de Registro de Preços.")
            print(f"{'='*50}\n")
            
            return True
            
        except Exception as e:
            print(f"Erro ao enviar relatório: {e}")
            return False
    
    def testar_configuracao(self) -> bool:
        """Testa a configuração do serviço de email"""
        print(f"\n{'='*50}")
        print("TESTE DE CONFIGURAÇÃO DE EMAIL")
        print(f"{'='*50}")
        print(f"Destinatários padrão: {', '.join(self.destinatarios_padrao)}")
        print(f"Status: Configuração OK (modo simulação)")
        print(f"Data/Hora: {date.today().strftime('%d/%m/%Y')}")
        print(f"{'='*50}\n")
        return True

