class InformeStateError(Exception):
    pass


class BaseInformeState:
    value = None
    allowed_transitions = set()

    def can_transition_to(self, next_state):
        return next_state in self.allowed_transitions

    def transition(self, informe, next_state):
        if not self.can_transition_to(next_state):
            raise InformeStateError(
                f"No se puede cambiar de '{self.value}' a '{next_state}'."
            )
        informe.estado = next_state
        return informe


class EnviadoState(BaseInformeState):
    value = 'enviado'
    allowed_transitions = {'pendiente_secretaria'}


class PendienteSecretariaState(BaseInformeState):
    value = 'pendiente_secretaria'
    allowed_transitions = {'pendiente_presidente'}


class PendientePresidenteState(BaseInformeState):
    value = 'pendiente_presidente'
    allowed_transitions = {'pendiente_docente'}


class PendienteDocenteState(BaseInformeState):
    value = 'pendiente_docente'
    allowed_transitions = {'validando_ia'}


class ValidandoIAState(BaseInformeState):
    value = 'validando_ia'
    allowed_transitions = {'revision_docente'}


class RevisionDocenteState(BaseInformeState):
    value = 'revision_docente'
    allowed_transitions = {'pendiente_aprobacion_presidente', 'rechazado_estudiante'}


class PendienteAprobacionPresidenteState(BaseInformeState):
    value = 'pendiente_aprobacion_presidente'
    allowed_transitions = {'aprobado_presidente', 'rechazado_presidente'}


class AprobadoPresidenteState(BaseInformeState):
    value = 'aprobado_presidente'
    allowed_transitions = {'aprobado_final'}


class RechazadoPresidenteState(BaseInformeState):
    value = 'rechazado_presidente'
    allowed_transitions = {'validando_ia', 'revision_docente'}


class AprobadoFinalState(BaseInformeState):
    value = 'aprobado_final'
    allowed_transitions = set()  # Estado final


class RechazadoEstudianteState(BaseInformeState):
    value = 'rechazado_estudiante'
    allowed_transitions = {'enviado'}  # El estudiante puede reenviar


STATE_MAP = {
    'enviado': EnviadoState(),
    'pendiente_secretaria': PendienteSecretariaState(),
    'pendiente_presidente': PendientePresidenteState(),
    'pendiente_docente': PendienteDocenteState(),
    'validando_ia': ValidandoIAState(),
    'revision_docente': RevisionDocenteState(),
    'pendiente_aprobacion_presidente': PendienteAprobacionPresidenteState(),
    'aprobado_presidente': AprobadoPresidenteState(),
    'rechazado_presidente': RechazadoPresidenteState(),
    'aprobado_final': AprobadoFinalState(),
    'rechazado_estudiante': RechazadoEstudianteState(),
}


def get_state(state_value: str) -> BaseInformeState:
    try:
        return STATE_MAP[state_value]
    except KeyError as exc:
        raise InformeStateError(f"Estado desconocido: {state_value}") from exc
