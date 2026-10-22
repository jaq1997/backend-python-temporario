import { useState } from 'react';
import { UserContext } from './userContextStore';

export function UserProvider({ children }) {
  const [usuario, setUsuario] = useState(() => {
    const usuarioSalvo = localStorage.getItem('informa-saude-usuario-ativo');
    if (usuarioSalvo) {
      try {
        return JSON.parse(usuarioSalvo);
      } catch {
        return { nome: usuarioSalvo, email: 'joaodasilva@example.com' };
      }
    }
    return { nome: 'João da Silva', email: 'joaodasilva@example.com' };
  });

  const [jornadaRecomendada, setJornadaRecomendada] = useState(() => {
    return localStorage.getItem('informa-saude-jornada-destaque') || null;
  });

  const atualizarUsuario = (novosDados) => {
    setUsuario((prev) => {
      const atualizado = { ...prev, ...novosDados };
      localStorage.setItem('informa-saude-usuario-ativo', JSON.stringify(atualizado));
      return atualizado;
    });
  };

  const atualizarJornada = (jornadaKey) => {
    setJornadaRecomendada(jornadaKey);
    if (jornadaKey) {
      localStorage.setItem('informa-saude-jornada-destaque', jornadaKey);
    } else {
      localStorage.removeItem('informa-saude-jornada-destaque');
    }
  };

  return (
    <UserContext.Provider value={{ usuario, atualizarUsuario, jornadaRecomendada, atualizarJornada }}>
      {children}
    </UserContext.Provider>
  );
}
