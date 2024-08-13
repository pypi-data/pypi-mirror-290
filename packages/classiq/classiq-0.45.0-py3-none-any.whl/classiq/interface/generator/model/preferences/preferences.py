from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

import pydantic
from typing_extensions import TypeAlias

from classiq.interface.backend.backend_preferences import (
    BackendPreferences,
    validate_backend_service_provider,
)
from classiq.interface.backend.quantum_backend_providers import (
    AllBackendsNameByVendor,
    ProviderVendor,
)
from classiq.interface.enum_utils import StrEnum
from classiq.interface.exceptions import ClassiqValueError
from classiq.interface.generator.arith.machine_precision import (
    DEFAULT_MACHINE_PRECISION,
)
from classiq.interface.generator.hardware.hardware_data import (
    BACKEND_VALIDATION_ERROR_MESSAGE,
    CustomHardwareSettings,
)
from classiq.interface.generator.model.preferences.randomness import create_random_seed
from classiq.interface.hardware import Provider
from classiq.interface.helpers.custom_pydantic_types import PydanticMachinePrecision

if TYPE_CHECKING:
    VisualizationLevel: TypeAlias = Optional[int]
else:
    VisualizationLevel: TypeAlias = Optional[pydantic.conint(ge=-1)]

if TYPE_CHECKING:
    PydanticBackendName = str
else:
    PydanticBackendName = pydantic.constr(
        strict=True, min_length=1, regex="^([.A-Za-z0-9_-]*)$"
    )


class QuantumFormat(StrEnum):
    QASM = "qasm"
    QSHARP = "qsharp"
    QIR = "qir"
    IONQ = "ionq"
    CIRQ_JSON = "cirq_json"
    QASM_CIRQ_COMPATIBLE = "qasm_cirq_compatible"


_SERVICE_PROVIDER_TO_FORMAT: Dict[Provider, QuantumFormat] = {
    Provider.CLASSIQ: QuantumFormat.QASM,
    Provider.IONQ: QuantumFormat.IONQ,
    Provider.AZURE_QUANTUM: QuantumFormat.QSHARP,
    Provider.IBM_QUANTUM: QuantumFormat.QASM,
    Provider.AMAZON_BRAKET: QuantumFormat.QASM,
}

if TYPE_CHECKING:
    PydanticConstrainedQuantumFormatList = List[QuantumFormat]
else:
    PydanticConstrainedQuantumFormatList = pydantic.conlist(
        QuantumFormat, min_items=1, max_items=len(QuantumFormat)
    )


class TranspilationOption(StrEnum):
    NONE = "none"
    DECOMPOSE = "decompose"
    AUTO_OPTIMIZE = "auto optimize"
    LIGHT = "light"
    MEDIUM = "medium"
    INTENSIVE = "intensive"
    CUSTOM = "custom"

    def __bool__(self) -> bool:
        return self != TranspilationOption.NONE


class Preferences(pydantic.BaseModel, extra=pydantic.Extra.forbid):
    _backend_preferences: Optional[BackendPreferences] = pydantic.PrivateAttr(
        default=None
    )
    machine_precision: PydanticMachinePrecision = DEFAULT_MACHINE_PRECISION

    backend_service_provider: Optional[Union[Provider, ProviderVendor, str]] = (
        pydantic.Field(
            default=None,
            description="Provider company or cloud for the requested backend.",
        )
    )
    backend_name: Optional[Union[PydanticBackendName, AllBackendsNameByVendor]] = (
        pydantic.Field(
            default=None, description="Name of the requested backend or target."
        )
    )
    custom_hardware_settings: CustomHardwareSettings = pydantic.Field(
        default_factory=CustomHardwareSettings,
        description="Custom hardware settings which will be used during optimization. "
        "This field is ignored if backend preferences are given.",
    )
    debug_mode: bool = pydantic.Field(
        default=True,
        description="Add debug information to the synthesized result. "
        "Setting this option to False can potentially speed up the synthesis, and is "
        "recommended for executing iterative algorithms.",
    )
    output_format: PydanticConstrainedQuantumFormatList = pydantic.Field(
        default=[QuantumFormat.QASM],
        description="The quantum circuit output format(s). ",
    )

    pretty_qasm: bool = pydantic.Field(
        True,
        description="Prettify the OpenQASM2 outputs (use line breaks inside the gate "
        "declarations).",
    )

    qasm3: Optional[bool] = pydantic.Field(
        None,
        description="Output OpenQASM 3.0 instead of OpenQASM 2.0. Relevant only for "
        "the `qasm` and `transpiled_circuit.qasm` attributes of `GeneratedCircuit`.",
    )

    transpilation_option: TranspilationOption = pydantic.Field(
        default=TranspilationOption.AUTO_OPTIMIZE,
        description="If true, the returned result will contain a "
        "transpiled circuit and its depth",
    )

    solovay_kitaev_max_iterations: Optional[pydantic.PositiveInt] = pydantic.Field(
        None,
        description="Maximum iterations for the Solovay-Kitaev algorithm (if applied).",
    )

    timeout_seconds: pydantic.PositiveInt = pydantic.Field(
        default=300, description="Generation timeout in seconds"
    )

    optimization_timeout_seconds: Optional[pydantic.PositiveInt] = pydantic.Field(
        default=None,
        description="Optimization timeout in seconds, or None for no "
        "optimization timeout (will still timeout when the generation timeout is over)",
    )

    random_seed: int = pydantic.Field(
        default_factory=create_random_seed,
        description="The random seed used for the generation",
    )

    @pydantic.validator("backend_service_provider", pre=True)
    def validate_backend_service_provider(
        cls, backend_service_provider: Any
    ) -> Optional[Provider]:
        if backend_service_provider is None:
            return None
        return validate_backend_service_provider(backend_service_provider)

    @pydantic.validator("optimization_timeout_seconds")
    def optimization_timeout_less_than_generation_timeout(
        cls,
        optimization_timeout_seconds: Optional[pydantic.PositiveInt],
        values: Dict[str, Any],
    ) -> Optional[pydantic.PositiveInt]:
        generation_timeout_seconds = values.get("timeout_seconds")
        if generation_timeout_seconds is None or optimization_timeout_seconds is None:
            return optimization_timeout_seconds
        if optimization_timeout_seconds >= generation_timeout_seconds:
            raise ClassiqValueError(
                f"Generation timeout ({generation_timeout_seconds})"
                f"is greater than or equal to "
                f"optimization timeout ({optimization_timeout_seconds}) "
            )
        return optimization_timeout_seconds

    @pydantic.validator("output_format", pre=True)
    def make_output_format_list(cls, output_format: Any) -> List:
        if not pydantic.utils.sequence_like(output_format):
            output_format = [output_format]

        return output_format

    @pydantic.validator("output_format", always=True)
    def validate_output_format(
        cls, output_format: PydanticConstrainedQuantumFormatList, values: Dict[str, Any]
    ) -> PydanticConstrainedQuantumFormatList:
        if len(output_format) != len(set(output_format)):
            raise ClassiqValueError(
                f"output_format={output_format}\n"
                "has at least one format that appears twice or more"
            )

        service_provider = values.get("backend_service_provider")
        if service_provider is None:
            return output_format

        provider_format = _SERVICE_PROVIDER_TO_FORMAT.get(service_provider)
        if provider_format is not None and provider_format not in output_format:
            output_format.append(provider_format)

        return output_format

    @pydantic.root_validator()
    def validate_backend(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        backend_name = values.get("backend_name")
        backend_service_provider = values.get("backend_service_provider")
        if (backend_name is None) != (backend_service_provider is None):
            raise ClassiqValueError(BACKEND_VALIDATION_ERROR_MESSAGE)
        return values

    @property
    def backend_preferences(self) -> Optional[BackendPreferences]:
        if self.backend_name is None or self.backend_service_provider is None:
            return None
        if self._backend_preferences is None:
            self._backend_preferences = BackendPreferences(
                backend_name=self.backend_name,
                backend_service_provider=self.backend_service_provider,
            )
        return self._backend_preferences
