import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, CheckCircle2, Loader2 } from 'lucide-react';
import { BarraAcessibilidade, BotaoSistema, OpcaoCard, Logo } from '../../components';
import { useUser } from '../../context/UserContext';

const PERGUNTAS = [
  // ── JORNADA CARDÍACA (1 a 3) ──
  {
    id: 1,
    jornada: 'cardiaca',
    titulo: 'Pergunta Cardíaca 1',
    subtitulo: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    opcoes: [
      { id: 'a', titulo: 'Resposta 1 (Lorem Ipsum)', descricao: 'Consectetur adipiscing elit, sed do eiusmod tempor.' },
      { id: 'b', titulo: 'Resposta 2 (Lorem Ipsum)', descricao: 'Ut enim ad minim veniam, quis nostrud exercitation.' },
      { id: 'c', titulo: 'Resposta 3 (Lorem Ipsum)', descricao: 'Duis aute irure dolor in reprehenderit in voluptate.' },
      { id: 'd', titulo: 'Resposta 4 (Lorem Ipsum)', descricao: 'Sunt in culpa qui officia deserunt mollit anim id est.' },
    ]
  },
  {
    id: 2,
    jornada: 'cardiaca',
    titulo: 'Pergunta Cardíaca 2',
    subtitulo: 'Integer nec odio. Praesent libero. Sed cursus ante dapibus diam.',
    opcoes: [
      { id: 'a', titulo: 'Resposta 1 (Lorem Ipsum)', descricao: 'Nulla pariatur excepteur sint occaecat cupidatat non proident.' },
      { id: 'b', titulo: 'Resposta 2 (Lorem Ipsum)', descricao: 'Mollit anim id est laborum et dolorum fuga harum quidem.' },
      { id: 'c', titulo: 'Resposta 3 (Lorem Ipsum)', descricao: 'Voluptas sit aspernatur aut odit aut fugit sed quia consequuntur.' },
      { id: 'd', titulo: 'Resposta 4 (Lorem Ipsum)', descricao: 'Dolorem ipsum quia dolor sit amet consectetur adipisci velit.' },
    ]
  },
  {
    id: 3,
    jornada: 'cardiaca',
    titulo: 'Pergunta Cardíaca 3',
    subtitulo: 'Sed nisi. Nulla quis sem at nibh elementum imperdiet.',
    opcoes: [
      { id: 'a', titulo: 'Resposta 1 (Lorem Ipsum)', descricao: 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem.' },
      { id: 'b', titulo: 'Resposta 2 (Lorem Ipsum)', descricao: 'Laudantium totam rem aperiam eaque ipsa quae ab illo inventore.' },
      { id: 'c', titulo: 'Resposta 3 (Lorem Ipsum)', descricao: 'Veritatis et quasi architecto beatae vitae dicta sunt explicabo.' },
      { id: 'd', titulo: 'Resposta 4 (Lorem Ipsum)', descricao: 'Nemo enim ipsam voluptatem quia voluptas sit aspernatur.' },
    ]
  },
  // ── JORNADA DO SONO (4 a 6) ──
  {
    id: 4,
    jornada: 'sono',
    titulo: 'Pergunta do Sono 1',
    subtitulo: 'Duis sagittis ipsum. Praesent mauris. Fusce nec tellus sed augue semper porta.',
    opcoes: [
      { id: 'a', titulo: 'Resposta 1 (Lorem Ipsum)', descricao: 'Neque porro quisquam est qui dolorem ipsum quia dolor sit amet.' },
      { id: 'b', titulo: 'Resposta 2 (Lorem Ipsum)', descricao: 'Consectetur adipisci velit sed quia non numquam eius modi tempora.' },
      { id: 'c', titulo: 'Resposta 3 (Lorem Ipsum)', descricao: 'Incidunt ut labore et dolore magnam aliquam quaerat voluptatem.' },
      { id: 'd', titulo: 'Resposta 4 (Lorem Ipsum)', descricao: 'Ut enim ad minima veniam quis nostrum exercitationem ullam.' },
    ]
  },
  {
    id: 5,
    jornada: 'sono',
    titulo: 'Pergunta do Sono 2',
    subtitulo: 'Mauris massa. Vestibulum lacinia arcu eget nulla. Class aptent taciti.',
    opcoes: [
      { id: 'a', titulo: 'Resposta 1 (Lorem Ipsum)', descricao: 'Corporis suscipit laboriosam nisi ut aliquid ex ea commodi consequatur.' },
      { id: 'b', titulo: 'Resposta 2 (Lorem Ipsum)', descricao: 'Quis autem vel eum iure reprehenderit qui in ea voluptate velit.' },
      { id: 'c', titulo: 'Resposta 3 (Lorem Ipsum)', descricao: 'Esse quam nihil molestiae consequatur vel illum qui dolorem.' },
      { id: 'd', titulo: 'Resposta 4 (Lorem Ipsum)', descricao: 'Eum fugiat quo voluptas nulla pariatur at vero eos et accusamus.' },
    ]
  },
  {
    id: 6,
    jornada: 'sono',
    titulo: 'Pergunta do Sono 3',
    subtitulo: 'Curabitur sodales ligula in libero. Sed dignissim lacinia nunc.',
    opcoes: [
      { id: 'a', titulo: 'Resposta 1 (Lorem Ipsum)', descricao: 'Iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum.' },
      { id: 'b', titulo: 'Resposta 2 (Lorem Ipsum)', descricao: 'Deleniti atque corrupti quos dolores et quas molestias excepturi.' },
      { id: 'c', titulo: 'Resposta 3 (Lorem Ipsum)', descricao: 'Sint occaecati cupiditate non provident similique sunt in culpa.' },
      { id: 'd', titulo: 'Resposta 4 (Lorem Ipsum)', descricao: 'Qui officia deserunt mollitia animi id est laborum et dolorum fuga.' },
    ]
  },
  // ── JORNADA RESPIRATÓRIA (7 a 9) ──
  {
    id: 7,
    jornada: 'respiratoria',
    titulo: 'Pergunta Respiratória 1',
    subtitulo: 'Curabitur tortor. Pellentesque nibh. Aenean quam. In scelerisque sem at dolor.',
    opcoes: [
      { id: 'a', titulo: 'Resposta 1 (Lorem Ipsum)', descricao: 'Et harum quidem rerum facilis est et expedita distinctio nam libero.' },
      { id: 'b', titulo: 'Resposta 2 (Lorem Ipsum)', descricao: 'Tempore cum soluta nobis est eligendi optio cumque nihil impedit.' },
      { id: 'c', titulo: 'Resposta 3 (Lorem Ipsum)', descricao: 'Quo minus id quod maxime placeat facere possimus omnis voluptas.' },
      { id: 'd', titulo: 'Resposta 4 (Lorem Ipsum)', descricao: 'Assumenda est omnis dolor repellendus temporibus autem quibusdam.' },
    ]
  },
  {
    id: 8,
    jornada: 'respiratoria',
    titulo: 'Pergunta Respiratória 2',
    subtitulo: 'Maecenas mattis. Sed convallis tristique sem. Proin ut ligula vel nunc egestas porttitor.',
    opcoes: [
      { id: 'a', titulo: 'Resposta 1 (Lorem Ipsum)', descricao: 'Et aut officiis debitis aut rerum necessitatibus saepe eveniet.' },
      { id: 'b', titulo: 'Resposta 2 (Lorem Ipsum)', descricao: 'Ut et voluptates repudiandae sint et molestiae non recusandae.' },
      { id: 'c', titulo: 'Resposta 3 (Lorem Ipsum)', descricao: 'Itaque earum rerum hic tenetur a sapiente delectus ut aut reiciendis.' },
      { id: 'd', titulo: 'Resposta 4 (Lorem Ipsum)', descricao: 'Voluptatibus maiores alias consequatur aut perferendis doloribus asperiores.' },
    ]
  },
  {
    id: 9,
    jornada: 'respiratoria',
    titulo: 'Pergunta Respiratória 3',
    subtitulo: 'Morbi lectus risus, iaculis vel, suscipit quis, luctus non, massa. Fusce ac turpis.',
    opcoes: [
      { id: 'a', titulo: 'Resposta 1 (Lorem Ipsum)', descricao: 'Repellat nam libero tempore cum soluta nobis est eligendi optio.' },
      { id: 'b', titulo: 'Resposta 2 (Lorem Ipsum)', descricao: 'Cumque nihil impedit quo minus id quod maxime placeat facere possimus.' },
      { id: 'c', titulo: 'Resposta 3 (Lorem Ipsum)', descricao: 'Omnis voluptas assumenda est omnis dolor repellendus temporibus.' },
      { id: 'd', titulo: 'Resposta 4 (Lorem Ipsum)', descricao: 'Autem quibusdam et aut officiis debitis aut rerum necessitatibus.' },
    ]
  },
];

export function Questionario() {
  const navigate = useNavigate();
  const { atualizarJornada } = useUser();

  const [etapaAtual, setEtapaAtual] = useState(0);
  const [respostas, setRespostas] = useState({});
  const [isConcluindo, setIsConcluindo] = useState(false);
  const [jornadaRecomendada, setJornadaRecomendada] = useState(null);
  const [mensagemSucesso, setMensagemSucesso] = useState('');
  const [avisoPersistencia, setAvisoPersistencia] = useState('');

  const perguntaAtual = PERGUNTAS[etapaAtual];
  const opcaoSelecionada = respostas[perguntaAtual.id];
  const percentualProgresso = ((etapaAtual + 1) / PERGUNTAS.length) * 100;

  const handleSelecionarOpcao = (opcaoId) => {
    setRespostas(prev => ({
      ...prev,
      [perguntaAtual.id]: opcaoId
    }));
  };

  const handleAvancar = async () => {
    if (etapaAtual < PERGUNTAS.length - 1) {
      setEtapaAtual(prev => prev + 1);
    } else {
      setIsConcluindo(true);

      const pontos = { cardiaca: 0, sono: 0, respiratoria: 0 };
      const pesoOpcao = { a: 1, b: 2, c: 3, d: 4 };

      PERGUNTAS.forEach(p => {
        const opId = respostas[p.id];
        if (opId) {
          pontos[p.jornada] += pesoOpcao[opId];
        }
      });

      const prioridadeEmpate = ['cardiaca', 'respiratoria', 'sono'];
      let melhorJornada = prioridadeEmpate[0];
      for (const jornada of prioridadeEmpate.slice(1)) {
        if (pontos[jornada] > pontos[melhorJornada]) {
          melhorJornada = jornada;
        }
      }

      let usuarioId;
      try {
        const usuario = JSON.parse(localStorage.getItem('informa-saude-usuario-ativo') || 'null');
        const id = Number(usuario?.usuario_id);
        if (Number.isSafeInteger(id) && id > 0) usuarioId = id;
      } catch {
        usuarioId = undefined;
      }

      const concluirLocalmente = (aviso) => {
        setJornadaRecomendada(melhorJornada);
        setMensagemSucesso('Questionário concluído. Sua recomendação foi calculada com base nas respostas.');
        setAvisoPersistencia(aviso);
        atualizarJornada(melhorJornada);
      };

      if (!usuarioId) {
        concluirLocalmente(
          'Não foi possível salvar suas respostas na conta porque o ID do usuário ainda não está disponível.'
        );
        return;
      }

      try {
        const payload = {
          usuario_id: usuarioId,
          respostas: Object.fromEntries(
            Object.entries(respostas).map(([k, v]) => [String(k), v])
          )
        };

        const res = await fetch('http://localhost:8000/api/questionario/resultado', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        if (res.ok) {
          const dados = await res.json();
          setJornadaRecomendada(dados.jornada_recomendada);
          setMensagemSucesso(dados.mensagem);
          setAvisoPersistencia('');
          atualizarJornada(dados.jornada_recomendada);
        } else {
          concluirLocalmente('Não foi possível salvar suas respostas no servidor. Sua recomendação foi calculada neste dispositivo.');
        }
      } catch {
        concluirLocalmente('Não foi possível conectar ao servidor para salvar suas respostas. Sua recomendação foi calculada neste dispositivo.');
      }
    }
  };

  const handleVoltar = () => {
    if (etapaAtual > 0) {
      setEtapaAtual(prev => prev - 1);
    } else {
      navigate('/inicio');
    }
  };

  const nomesJornadas = {
    cardiaca: 'Jornada Cardíaca',
    sono: 'Jornada do Sono',
    respiratoria: 'Jornada Respiratória'
  };

  if (isConcluindo) {
    return (
      <div className="bg-light min-vh-100 d-flex flex-column justify-content-center align-items-center p-4">
        <div className="card border-0 shadow-sm p-4 p-md-5 text-center" style={{ maxWidth: '520px', borderRadius: '16px' }}>
          {!jornadaRecomendada ? (
            <div>
              <Loader2 size={48} className="text-is-green spin mb-3 mx-auto" />
              <h2 className="fw-bold fs-3 text-dark mb-2">Calculando sua melhor jornada...</h2>
              <p className="text-muted mb-0">Analisando suas respostas para recomendar a série ideal.</p>
            </div>
          ) : (
            <div>
              <CheckCircle2 size={56} className="text-success mb-3 mx-auto" />
              <h2 className="fw-bold fs-3 text-dark mb-2">Triagem Concluída!</h2>
              <p className="text-muted mb-3">{mensagemSucesso}</p>
              {avisoPersistencia && (
                <div className="alert alert-warning py-2 small" role="status">
                  {avisoPersistencia}
                </div>
              )}

              <div className="alert alert-success border-0 py-3 mb-4" style={{ backgroundColor: 'var(--is-green-light)' }}>
                <span className="d-block small text-muted text-uppercase fw-bold">Sua Jornada Principal</span>
                <span className="fs-4 fw-bold text-is-green">{nomesJornadas[jornadaRecomendada] || 'Jornada Cardíaca'}</span>
              </div>

              <BotaoSistema
                variante="orange"
                onClick={() => navigate('/inicio')}
              >
                Ver Minha Jornada na Home
              </BotaoSistema>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-light min-vh-100 d-flex flex-column justify-content-between pb-5">
      <div>
        <BarraAcessibilidade />

        <header className="bg-white border-bottom py-3 shadow-sm sticky-top">
          <div className="is-container">
            <div className="d-flex align-items-center justify-content-between mb-2">
              <button 
                type="button" 
                onClick={handleVoltar}
                className="btn btn-link text-decoration-none text-dark d-inline-flex align-items-center gap-2 p-0 fw-semibold fs-6"
                aria-label="Voltar para a pergunta anterior"
              >
                <ArrowLeft size={20} /> <span className="d-none d-sm-inline">Voltar</span>
              </button>

              <Logo to="/inicio" />

              <span className="fw-bold text-is-green fs-6">
                {etapaAtual + 1} de {PERGUNTAS.length}
              </span>
            </div>

            <div className="progress is-questionnaire-progress overflow-hidden rounded-pill">
              <div 
                className="progress-bar transition-all" 
                role="progressbar" 
                style={{ width: `${percentualProgresso}%` }} 
                aria-valuenow={percentualProgresso} 
                aria-valuemin="0" 
                aria-valuemax="100"
              ></div>
            </div>
          </div>
        </header>

        <main className="is-container py-4 py-md-5">
          <div className="row justify-content-center">
            <div className="col-12 col-md-10 col-lg-8 col-xl-7">
              <div className="text-center mb-4 pb-2">
                <h1 className="fw-bold text-dark fs-2 mb-2">{perguntaAtual.titulo}</h1>
                <p className="text-muted fs-5 mb-0">{perguntaAtual.subtitulo}</p>
              </div>

              <div 
                className="row row-cols-1 row-cols-md-2 g-3 mb-4" 
                role="radiogroup" 
                aria-label={perguntaAtual.titulo}
              >
                {perguntaAtual.opcoes.map((opcao) => (
                  <div key={opcao.id} className="col">
                    <OpcaoCard
                      titulo={opcao.titulo}
                      descricao={opcao.descricao}
                      selecionado={opcaoSelecionada === opcao.id}
                      onClick={() => handleSelecionarOpcao(opcao.id)}
                    />
                  </div>
                ))}
              </div>

              <div className="d-flex align-items-center justify-content-between mt-4 pt-2">
                <BotaoSistema
                  variante="outline-green"
                  onClick={handleVoltar}
                >
                  {etapaAtual === 0 ? 'Voltar' : 'Anterior'}
                </BotaoSistema>

                <BotaoSistema
                  variante={opcaoSelecionada ? 'orange' : 'secondary'}
                  desabilitado={!opcaoSelecionada}
                  onClick={handleAvancar}
                >
                  {etapaAtual === PERGUNTAS.length - 1 ? 'Concluir' : 'Seguinte'}
                </BotaoSistema>
              </div>

            </div>
          </div>
        </main>
      </div>

    </div>
  );
}

export default Questionario;
