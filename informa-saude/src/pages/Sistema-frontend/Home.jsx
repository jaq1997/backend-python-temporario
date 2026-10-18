import { useState } from 'react';
import { User, Gift, BookOpen, Hospital } from 'lucide-react';
import imgCardiaca from '../../assets/images/imagem-cardiaca.webp';
import imgSono from '../../assets/images/imagem-sono.webp';
import imgRespiracao from '../../assets/images/imagem-respiracao.webp';
import imgProgresso from '../../assets/images/acompanhe-progresso.webp';
import {
  SystemNavbar,
  CardSistema,
  FooterSistemaMobile,
  TituloPaginaSistema,
  TituloSecao,
  ModalRedeSaude,
} from '../../components';
import { obterNomeUsuario } from '../../utils/usuario';
import { useUser } from '../../context/UserContext';


const ACOES_RAPIDAS = [
  { id: 'jornadas', icone: BookOpen, titulo: 'Jornadas', href: '#jornadas' },
  { id: 'rede-publica', icone: Hospital, titulo: 'Rede Pública', href: '/404.html' },
  { id: 'pontos', icone: Gift, titulo: 'Pontos', href: '/404.html' },
  { id: 'perfil', icone: User, titulo: 'Meu Perfil', to: '/meu-perfil' }
];

const JORNADAS_EM_ANDAMENTO = [
  {
    id: 1,
    categoria: 'Hipertensão',
    titulo: 'Controlando o colesterol na alimentação',
    progresso: 65
  },
  {
    id: 2,
    categoria: 'Prevenção',
    titulo: 'Hábitos diários para o controle da glicemia',
    progresso: 30
  }
];

const JORNADAS_RECOMENDADAS = [
  {
    id: 'sono',
    imagem: imgSono,
    titulo: 'Jornada do Sono',
    descricao: 'Construa hábitos saudáveis e conheça práticas de higiene do sono para descansar melhor.',
    textoBotao: 'Iniciar Jornada'
  },
  {
    id: 'cardiaca',
    imagem: imgCardiaca,
    titulo: 'Jornada Cardíaca',
    descricao: 'Aprenda como pequenos hábitos diários podem auxiliar na prevenção e no cuidado cardiovascular.',
    textoBotao: 'Iniciar Jornada'
  },
  {
    id: 'respiratoria',
    imagem: imgRespiracao,
    titulo: 'Jornada Respiratória',
    descricao: 'Conheça práticas de respiração e cuidados diários para o bem-estar respiratório.',
    textoBotao: 'Iniciar Jornada'
  }
];

export function HomeSistema() {
  const nomeUsuario = obterNomeUsuario();
  const { jornadaRecomendada } = useUser();
  const [modalRedeAberto, setModalRedeAberto] = useState(false);
  const jornadaDestaque = JORNADAS_RECOMENDADAS.find(
    (jornada) => jornada.id === jornadaRecomendada
  ) || JORNADAS_RECOMENDADAS.find((jornada) => jornada.id === 'cardiaca');

  return (
    <div className="bg-light min-vh-100 pb-5">
      <SystemNavbar />

      <main className="is-container py-4">
        <TituloPaginaSistema
          isBoasVindas
          nome={nomeUsuario}
          subtitulo="Acesse suas jornadas, pontos e serviços de saúde"
        />

        <section className="mb-5">
          <TituloSecao>Ações Rápidas</TituloSecao>
          <div className="row g-3">
            {ACOES_RAPIDAS.map((acao) => (
              <div key={acao.id} className="col-6 col-md-4 col-lg-3">
                {acao.id === 'rede-publica' ? (
                  <div role="button" onClick={() => setModalRedeAberto(true)} style={{ cursor: 'pointer' }}>
                    <CardSistema isAcao icone={acao.icone} titulo={acao.titulo} />
                  </div>
                ) : (
                  <CardSistema isAcao icone={acao.icone} titulo={acao.titulo} href={acao.href} to={acao.to} />
                )}
              </div>
            ))}
          </div>
        </section>

        {/* Modal de Busca de UPAs e Hospitais (Geolocalização / ViaCEP) */}
        <ModalRedeSaude aberto={modalRedeAberto} aoFechar={() => setModalRedeAberto(false)} />


        <CardSistema
          isMedia
          isHero
          imagem={jornadaDestaque.imagem}
          subtitulo="Sua jornada recomendada"
          titulo={jornadaDestaque.titulo}
          descricao={jornadaDestaque.descricao}
          textoBotao={jornadaDestaque.textoBotao}
          to={`/jornada/${jornadaDestaque.id}`}
          className="mb-5"
        />

        <section className="mb-5">
          <TituloSecao>Continue Assistindo</TituloSecao>
          <div className="row g-3">
            {JORNADAS_EM_ANDAMENTO.map((jornada) => (
              <div key={jornada.id} className="col-12 col-md-6 col-lg-4">
                <CardSistema
                  isProgresso
                  categoria={jornada.categoria}
                  titulo={jornada.titulo}
                  progresso={jornada.progresso}
                  to="/jornada/cardiaca"
                />
              </div>
            ))}
          </div>
        </section>

        <section className="mb-5" id="jornadas">
          <TituloSecao>Jornadas Recomendadas</TituloSecao>
          <div className="row g-4">
            {JORNADAS_RECOMENDADAS.map((jornada) => (
              <div key={jornada.id} className="col-12 col-md-6 col-lg-4">
                <CardSistema
                  isMedia
                  imagem={jornada.imagem}
                  titulo={jornada.titulo}
                  textoBotao={jornada.textoBotao}
                  to={`/jornada/${jornada.id}`}
                />
              </div>
            ))}
          </div>
        </section>

        <section>
          <CardSistema
            isMedia
            centralizado
            imagem={imgProgresso}
            titulo="Acompanhe seu progresso"
            textoBotao="Veja suas estatísticas"
            varianteBotao="outline-white"
          />
        </section>
      </main>

      <FooterSistemaMobile />
    </div>
  );
}

export default HomeSistema;