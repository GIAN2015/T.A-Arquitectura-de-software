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
    allowed_transitions = {'validando'}


class ValidandoState(BaseInformeState):
    value = 'validando'
    allowed_transitions = {'observado', 'completado'}


class ObservadoState(BaseInformeState):
    value = 'observado'
    allowed_transitions = {'revision_docente', 'aprobado', 'rechazado'}


class RevisionDocenteState(BaseInformeState):
    value = 'revision_docente'
    allowed_transitions = {'aprobado', 'rechazado', 'observado'}


class RechazadoState(BaseInformeState):
    value = 'rechazado'
    allowed_transitions = {'enviado'}


class AprobadoState(BaseInformeState):
    value = 'aprobado'
    allowed_transitions = {'completado'}


class CompletadoState(BaseInformeState):
    value = 'completado'
    allowed_transitions = set()


STATE_MAP = {
    'enviado': EnviadoState(),
    'validando': ValidandoState(),
    'observado': ObservadoState(),
    'revision_docente': RevisionDocenteState(),
    'rechazado': RechazadoState(),
    'aprobado': AprobadoState(),
    'completado': CompletadoState(),
}


def get_state(state_value: str) -> BaseInformeState:
    try:
        return STATE_MAP[state_value]
    except KeyError as exc:
        raise InformeStateError(f"Estado desconocido: {state_value}") from exc
