########################
# Operation Classes    #
########################

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any, Dict, List
from app.exceptions import ValidationError


class Operation(ABC):
    """
    Abstract base class for calculator operations.

    Defines the interface for all arithmetic operations. Each operation must
    implement the execute method and can optionally override operand validation.
    """

    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Execute the operation.

        Performs the arithmetic operation on the provided operands.

        Args:
            a (Decimal): First operand.
            b (Decimal): Second operand.

        Returns:
            Decimal: Result of the operation.

        Raises:
            OperationError: If the operation fails.
        """
        pass  # pragma: no cover

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands before execution.

        Can be overridden by subclasses to enforce specific validation rules
        for different operations.

        Args:
            a (Decimal): First operand.
            b (Decimal): Second operand.

        Raises:
            ValidationError: If operands are invalid.
        """
        pass

    def __str__(self) -> str:
        """
        Return operation name for display.

        Provides a string representation of the operation, typically the class name.

        Returns:
            str: Name of the operation.
        """
        return self.__class__.__name__


########################
# Operation Registry    #
########################
#
# The registry populated via the `@register` class decorator below implements
# the Decorator pattern: rather than hand-maintaining a separate list of
# operations for the Factory *and* a separate hard-coded help string in the
# REPL, each Operation subclass announces its own command name and
# description at the point where it's defined. OperationFactory and the REPL
# help menu simply read from this registry, so adding a brand new operation
# is a single, self-contained change - decorate the class, and it
# automatically becomes creatable *and* shows up in `help`.

_OPERATION_REGISTRY: Dict[str, Dict[str, Any]] = {}


def register(name: str, description: str):
    """
    Class decorator that registers an Operation subclass for use by the
    calculator.

    Implements the Decorator design pattern: it wraps an Operation subclass
    definition to attach registration metadata (its command name and a
    human-readable description) without changing the class itself. This is
    what allows the REPL's help menu to be generated dynamically from
    whichever operations are currently registered, instead of being a static,
    manually maintained string.

    Args:
        name (str): The command identifier used to invoke the operation
            (e.g., 'add', 'modulus').
        description (str): A short, human-readable description shown in the
            REPL's dynamically generated help menu.

    Returns:
        Callable[[type], type]: A decorator that registers and returns the
        decorated class unchanged.

    Raises:
        TypeError: If applied to a class that does not inherit from
            Operation.
    """
    def decorator(operation_class: type) -> type:
        if not issubclass(operation_class, Operation):
            raise TypeError("Operation class must inherit from Operation")
        _OPERATION_REGISTRY[name.lower()] = {
            "class": operation_class,
            "description": description,
        }
        return operation_class
    return decorator


@register("add", "Add two numbers")
class Addition(Operation):
    """
    Addition operation implementation.

    Performs the addition of two numbers.
    """

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Add two numbers.

        Args:
            a (Decimal): First operand.
            b (Decimal): Second operand.

        Returns:
            Decimal: Sum of the two operands.
        """
        self.validate_operands(a, b)
        return a + b


@register("subtract", "Subtract the second number from the first")
class Subtraction(Operation):
    """
    Subtraction operation implementation.

    Performs the subtraction of one number from another.
    """

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Subtract one number from another.

        Args:
            a (Decimal): First operand.
            b (Decimal): Second operand.

        Returns:
            Decimal: Difference between the two operands.
        """
        self.validate_operands(a, b)
        return a - b


@register("multiply", "Multiply two numbers")
class Multiplication(Operation):
    """
    Multiplication operation implementation.

    Performs the multiplication of two numbers.
    """

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Multiply two numbers.

        Args:
            a (Decimal): First operand.
            b (Decimal): Second operand.

        Returns:
            Decimal: Product of the two operands.
        """
        self.validate_operands(a, b)
        return a * b


@register("divide", "Divide the first number by the second")
class Division(Operation):
    """
    Division operation implementation.

    Performs the division of one number by another.
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands, checking for division by zero.

        Overrides the base class method to ensure that the divisor is not zero.

        Args:
            a (Decimal): Dividend.
            b (Decimal): Divisor.

        Raises:
            ValidationError: If the divisor is zero.
        """
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Division by zero is not allowed")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Divide one number by another.

        Args:
            a (Decimal): Dividend.
            b (Decimal): Divisor.

        Returns:
            Decimal: Quotient of the division.
        """
        self.validate_operands(a, b)
        return a / b


@register("power", "Raise the first number to the power of the second")
class Power(Operation):
    """
    Power (exponentiation) operation implementation.

    Raises one number to the power of another.
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands for power operation.

        Overrides the base class method to ensure that the exponent is not negative.

        Args:
            a (Decimal): Base number.
            b (Decimal): Exponent.

        Raises:
            ValidationError: If the exponent is negative.
        """
        super().validate_operands(a, b)
        if b < 0:
            raise ValidationError("Negative exponents not supported")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Calculate one number raised to the power of another.

        Args:
            a (Decimal): Base number.
            b (Decimal): Exponent.

        Returns:
            Decimal: Result of the exponentiation.
        """
        self.validate_operands(a, b)
        return Decimal(pow(float(a), float(b)))


@register("root", "Calculate the nth root of a number")
class Root(Operation):
    """
    Root operation implementation.

    Calculates the nth root of a number.
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands for root operation.

        Overrides the base class method to ensure that the number is non-negative
        and the root degree is not zero.

        Args:
            a (Decimal): Number from which the root is taken.
            b (Decimal): Degree of the root.

        Raises:
            ValidationError: If the number is negative or the root degree is zero.
        """
        super().validate_operands(a, b)
        if a < 0:
            raise ValidationError("Cannot calculate root of negative number")
        if b == 0:
            raise ValidationError("Zero root is undefined")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Calculate the nth root of a number.

        Args:
            a (Decimal): Number from which the root is taken.
            b (Decimal): Degree of the root.

        Returns:
            Decimal: Result of the root calculation.
        """
        self.validate_operands(a, b)
        return Decimal(pow(float(a), 1 / float(b)))


@register("modulus", "Compute the remainder of dividing the first number by the second")
class Modulus(Operation):
    """
    Modulus operation implementation.

    Computes the remainder left over after dividing one number by another.
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands, checking for modulus by zero.

        Overrides the base class method to ensure that the divisor is not zero.

        Args:
            a (Decimal): Dividend.
            b (Decimal): Divisor.

        Raises:
            ValidationError: If the divisor is zero.
        """
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Modulus by zero is not allowed")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Calculate the remainder of dividing one number by another.

        Args:
            a (Decimal): Dividend.
            b (Decimal): Divisor.

        Returns:
            Decimal: Remainder of the division.
        """
        self.validate_operands(a, b)
        return a % b


@register("int_divide", "Divide and discard the remainder (integer division)")
class IntegerDivision(Operation):
    """
    Integer division operation implementation.

    Divides one number by another and discards any fractional remainder,
    returning only the integer quotient.
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands, checking for division by zero.

        Overrides the base class method to ensure that the divisor is not zero.

        Args:
            a (Decimal): Dividend.
            b (Decimal): Divisor.

        Raises:
            ValidationError: If the divisor is zero.
        """
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Integer division by zero is not allowed")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Divide one number by another, discarding the remainder.

        Args:
            a (Decimal): Dividend.
            b (Decimal): Divisor.

        Returns:
            Decimal: Integer quotient of the division.
        """
        self.validate_operands(a, b)
        return a // b


@register("percent", "Calculate what percentage the first number is of the second")
class Percentage(Operation):
    """
    Percentage operation implementation.

    Calculates what percentage the first number (a) represents of the
    second number (b), computed as (a / b) * 100.
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands, checking that the base (denominator) is not zero.

        Overrides the base class method to ensure that the percentage base
        is not zero, since that would require dividing by zero.

        Args:
            a (Decimal): The part.
            b (Decimal): The whole/base to compare against.

        Raises:
            ValidationError: If the base is zero.
        """
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Cannot calculate percentage with a base of zero")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Calculate what percentage a is of b.

        Args:
            a (Decimal): The part.
            b (Decimal): The whole/base to compare against.

        Returns:
            Decimal: The percentage value, i.e. (a / b) * 100.
        """
        self.validate_operands(a, b)
        return (a / b) * 100


@register("abs_diff", "Calculate the absolute difference between two numbers")
class AbsoluteDifference(Operation):
    """
    Absolute difference operation implementation.

    Calculates the absolute value of the difference between two numbers,
    so the result is always non-negative regardless of operand order.
    """

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Calculate the absolute difference between two numbers.

        Args:
            a (Decimal): First operand.
            b (Decimal): Second operand.

        Returns:
            Decimal: Absolute value of (a - b).
        """
        self.validate_operands(a, b)
        return abs(a - b)


class OperationFactory:
    """
    Factory class for creating operation instances.

    Implements the Factory pattern by providing a method to instantiate
    different operation classes based on a given operation type. This promotes
    scalability and decouples the creation logic from the Calculator class.

    Operation classes register themselves via the `@register` decorator
    (see above), so this factory's lookup table - and the descriptions used
    to build the REPL's dynamic help menu - stay in sync with whatever
    operations actually exist without any manual bookkeeping here.
    """

    # All lookups below read directly from the module-level
    # `_OPERATION_REGISTRY` rather than caching a copy of it. The registry is
    # populated live by the `@register` decorator as each Operation subclass
    # is defined, so reading it directly (instead of snapshotting it once at
    # class-definition time) is what makes newly decorated operations show up
    # immediately - including ones registered after this module was imported.

    @classmethod
    def register_operation(cls, name: str, operation_class: type, description: str = "Custom operation") -> None:
        """
        Register a new operation type.

        Allows dynamic addition of new operations to the factory. This is the
        imperative equivalent of the `@register` decorator, for cases where
        decorating the class definition isn't convenient (e.g. registering a
        class defined elsewhere, or at runtime).

        Args:
            name (str): Operation identifier (e.g., 'modulus').
            operation_class (type): The class implementing the new operation.
            description (str): Human-readable description shown in the
                REPL's dynamically generated help menu.

        Raises:
            TypeError: If the operation_class does not inherit from Operation.
        """
        if not issubclass(operation_class, Operation):
            raise TypeError("Operation class must inherit from Operation")
        _OPERATION_REGISTRY[name.lower()] = {
            "class": operation_class,
            "description": description,
        }

    @classmethod
    def create_operation(cls, operation_type: str) -> Operation:
        """
        Create an operation instance based on the operation type.

        This method retrieves the appropriate operation class from the
        operation registry and instantiates it.

        Args:
            operation_type (str): The type of operation to create (e.g., 'add').

        Returns:
            Operation: An instance of the specified operation class.

        Raises:
            ValueError: If the operation type is unknown.
        """
        entry = _OPERATION_REGISTRY.get(operation_type.lower())
        if not entry:
            raise ValueError(f"Unknown operation: {operation_type}")
        return entry["class"]()

    @classmethod
    def get_operation_names(cls) -> List[str]:
        """
        List every currently registered operation identifier.

        Used by the REPL to recognize which commands are calculations,
        instead of hard-coding the list of operation names.

        Returns:
            list[str]: Operation identifiers in registration order.
        """
        return list(_OPERATION_REGISTRY.keys())

    @classmethod
    def get_help_text(cls) -> str:
        """
        Build a human-readable help line for every registered operation.

        This is the core of the dynamic help menu: because it reads directly
        from the live operation registry (populated by the `@register`
        decorator), any newly added operation automatically appears here
        with no changes needed to the REPL itself.

        Returns:
            str: A comma-separated list of operation names followed by a
            combined description, formatted for display in the REPL's
            `help` command.
        """
        names = ", ".join(_OPERATION_REGISTRY.keys())
        return f"  {names} - Perform calculations"

    @classmethod
    def get_detailed_help_text(cls) -> str:
        """
        Build a multi-line help block describing each operation individually.

        Returns:
            str: One line per registered operation in the form
            "  <name> - <description>".
        """
        return "\n".join(
            f"  {name} - {meta['description']}"
            for name, meta in _OPERATION_REGISTRY.items()
        )
