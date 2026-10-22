import { useState } from 'react';
import { ModalSistema } from './ModalSistema';
import { FormInput } from '../FormInput/FormInput';
import { BotaoSistema } from '../Botao/BotaoSistema';

export function ModalAlterarSenha({ aberto = false, onClose, onSalvo }) {
  const [senhaAtual, setSenhaAtual] = useState('');
  const [novaSenha, setNovaSenha] = useState('');
  const [confirmarSenha, setConfirmarSenha] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setSenhaAtual('');
    setNovaSenha('');
    setConfirmarSenha('');
    if (onSalvo) onSalvo();
    onClose();
  };

  return (
    <ModalSistema aberto={aberto} onClose={onClose} titulo="Alterar Senha" tamanho="sm">
      <form onSubmit={handleSubmit}>
        <div className="mb-2">
          <FormInput
            id="senha-atual"
            label="Senha Atual"
            type="password"
            isPasswordToggle
            placeholder="Digite sua senha atual"
            value={senhaAtual}
            onChange={(e) => setSenhaAtual(e.target.value)}
            required
          />
        </div>

        <div className="mb-2">
          <FormInput
            id="nova-senha"
            label="Nova Senha"
            type="password"
            isPasswordToggle
            placeholder="Digite a nova senha"
            value={novaSenha}
            onChange={(e) => setNovaSenha(e.target.value)}
            required
          />
        </div>

        <div className="mb-3">
          <FormInput
            id="confirmar-nova-senha"
            label="Confirmar Nova Senha"
            type="password"
            isPasswordToggle
            placeholder="Confirme a nova senha"
            value={confirmarSenha}
            onChange={(e) => setConfirmarSenha(e.target.value)}
            required
          />
        </div>

        <div className="is-modal-actions">
          <BotaoSistema variante="orange" tipo="submit" className="fs-6">
            Salvar Nova Senha
          </BotaoSistema>
          <BotaoSistema variante="outline-green" tipo="button" className="fs-6" onClick={onClose}>
            Cancelar
          </BotaoSistema>
        </div>
      </form>
    </ModalSistema>
  );
}

export default ModalAlterarSenha;
