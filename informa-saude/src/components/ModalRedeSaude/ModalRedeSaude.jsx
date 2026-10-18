import { useState } from 'react';
import { MapPin, Search, Navigation, Phone, Clock, AlertCircle, Loader2 } from 'lucide-react';
import { ModalSistema } from '../ModalSistema/ModalSistema';

export function ModalRedeSaude({ aberto, aoFechar }) {
  const [estabelecimentos, setEstabelecimentos] = useState([]);
  const [carregando, setCarregando] = useState(false);
  const [buscaRealizada, setBuscaRealizada] = useState(false);
  const [erro, setErro] = useState('');
  const [cep, setCep] = useState('');

  const buscarPorGPS = () => {
    setCarregando(true);
    setErro('');
    setEstabelecimentos([]);
    setBuscaRealizada(false);

    if (!navigator.geolocation) {
      setErro('Seu navegador não suporta geolocalização. Por favor, busque pelo CEP.');
      setCarregando(false);
      return;
    }

    navigator.geolocation.getCurrentPosition(
      async (posicao) => {
        const { latitude, longitude } = posicao.coords;
        try {
          let url = `http://localhost:8000/api/estabelecimentos/proximos?lat=${latitude}&lng=${longitude}&raio=20`;

          const res = await fetch(url);
          if (!res.ok) throw new Error('Erro ao buscar estabelecimentos próximos.');
          const dados = await res.json();
          setEstabelecimentos(dados);
          setBuscaRealizada(true);
        } catch {
          setErro('Não foi possível conectar ao backend ou carregar estabelecimentos.');
        } finally {
          setCarregando(false);
        }
      },
      (err) => {
        const mensagem = err.code === 1
          ? 'Permissão de localização negada. Digite seu CEP abaixo para buscar.'
          : 'Não foi possível obter sua localização. Digite seu CEP abaixo para buscar.';
        setErro(mensagem);
        setCarregando(false);
      },
      { timeout: 10000 }
    );
  };

  const buscarPorCep = async (e) => {
    e?.preventDefault();
    const cepLimpo = cep.replace(/\D/g, '');
    if (cepLimpo.length !== 8) {
      setErro('Digite um CEP válido com 8 dígitos.');
      return;
    }

    setCarregando(true);
    setErro('');
    setEstabelecimentos([]);
    setBuscaRealizada(false);

    try {
      let url = `http://localhost:8000/api/estabelecimentos/por-cep?cep=${cepLimpo}&raio=20`;

      const res = await fetch(url);
      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || 'CEP não encontrado.');
      }
      const dados = await res.json();
      setEstabelecimentos(dados);
      setBuscaRealizada(true);
    } catch (e) {
      setErro(e.message || 'Erro ao buscar pelo CEP.');
    } finally {
      setCarregando(false);
    }
  };

  return (
    <ModalSistema aberto={aberto} aoFechar={aoFechar} titulo="Rede de Saúde — UPAs e Hospitais">
      <div className="p-3">
        <p className="text-muted small mb-3">
          Encontre UPAs e hospitais próximos de você em Porto Alegre, em um raio de até 20 km.
        </p>

        <div className="d-grid gap-2 mb-3">
          <button
            type="button"
            onClick={buscarPorGPS}
            disabled={carregando}
            className="btn btn-outline-success d-flex align-items-center justify-content-center gap-2 py-2 fw-semibold"
          >
            <Navigation size={18} /> Usar Minha Localização Atual
          </button>
        </div>

        <div className="position-relative text-center my-3">
          <hr />
          <span className="position-absolute top-50 start-50 translate-middle bg-white px-3 text-muted small">
            ou digite seu CEP
          </span>
        </div>

        <form onSubmit={buscarPorCep} className="row g-2 mb-3">
          <div className="col-8">
            <input
              type="text"
              className="form-control"
              placeholder="Ex: 90040-192"
              value={cep}
              maxLength={9}
              onChange={(e) => setCep(e.target.value)}
            />
          </div>
          <div className="col-4">
            <button
              type="submit"
              disabled={carregando || !cep.trim()}
              className="btn btn-primary w-100 d-flex align-items-center justify-content-center gap-1"
              style={{ backgroundColor: 'var(--is-green)', borderColor: 'var(--is-green)' }}
            >
              <Search size={16} /> Buscar
            </button>
          </div>
        </form>

        {erro && (
          <div className="alert alert-warning py-2 small d-flex align-items-center gap-2 mb-3">
            <AlertCircle size={16} className="text-warning flex-shrink-0" />
            <span>{erro}</span>
          </div>
        )}

        {carregando && (
          <div className="text-center py-4">
            <Loader2 size={32} className="spin text-is-green mx-auto mb-2" />
            <p className="text-muted small mb-0">Calculando unidades mais próximas...</p>
          </div>
        )}

        {!carregando && estabelecimentos.length > 0 && (
          <div className="mt-3" style={{ maxHeight: '350px', overflowY: 'auto' }}>
            <span className="small text-muted fw-bold d-block mb-2">
              {estabelecimentos.length} unidades encontradas:
            </span>
            <div className="d-flex flex-column gap-2">
              {estabelecimentos.map((est) => (
                <div key={est.id} className="card border p-3 shadow-sm rounded-3">
                  <div className="d-flex justify-content-between align-items-start gap-2 mb-1">
                    <h6 className="fw-bold text-dark mb-0">{est.nome}</h6>
                    {est.distancia_km !== null && (
                      <span className="badge bg-success-subtle text-success border border-success-subtle px-2 py-1">
                        {est.distancia_km} km
                      </span>
                    )}
                  </div>
                  <span className="badge bg-secondary-subtle text-secondary w-auto align-self-start mb-2">
                    {est.tipo}
                  </span>
                  <div className="small text-muted d-flex align-items-center gap-1 mb-1">
                    <MapPin size={14} className="flex-shrink-0 text-is-green" />
                    <span>{est.endereco} {est.bairro ? `— ${est.bairro}` : ''}</span>
                  </div>
                  {est.telefone && (
                    <div className="small text-muted d-flex align-items-center gap-1 mb-1">
                      <Phone size={14} className="flex-shrink-0" />
                      <span>{est.telefone}</span>
                    </div>
                  )}
                  {est.horario_funcionamento && (
                    <div className="small text-muted d-flex align-items-center gap-1">
                      <Clock size={14} className="flex-shrink-0" />
                      <span>{est.horario_funcionamento}</span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
        {!carregando && !erro && estabelecimentos.length === 0 && (
          <p className="text-muted small text-center mb-0">
            {buscaRealizada
              ? 'Nenhuma UPA ou hospital foi encontrado no raio de 20 km.'
              : 'Use sua localização ou informe um CEP para encontrar estabelecimentos próximos.'}
          </p>
        )}
      </div>
    </ModalSistema>
  );
}

export default ModalRedeSaude;
