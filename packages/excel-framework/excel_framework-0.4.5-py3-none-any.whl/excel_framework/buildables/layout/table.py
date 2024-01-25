from ...internals.buildable import Buildable
from overrides import override
from dataclasses import dataclass
from typing import Generic, TypeVar, Callable, Any, Union
from .column import Column
from .row import Row
from ..non_layout.excel_cell import ExcelCell
from ...styling.style import Style
from ...styling.styler import Styler, ConditionalStyler
from ...internals.build_context import BuildContext
from ...sizes.dimension import ColumnDimension, AutoWidth, FixedWidth

T = TypeVar("T")

@dataclass(frozen=True)
class ModelConditionalStyle(Generic[T]):
    styles: list[Style]
    selector: Callable[[T], Union[int, None]]

@dataclass(frozen=True)
class ValueConditionalStyle(Generic[T]):
    styles: list[Style]
    selector: Callable[[T], Union[int, None]]



@dataclass(frozen=True)
class TableColumn(Generic[T]):
    name: str
    value: Callable[[T], Any]
    width: Union[AutoWidth, FixedWidth, None] = None
    column_name_style: Union[Style, None] = None
    value_style: Union[Style, None] = None
    conditional_style: Union[ModelConditionalStyle[T], ValueConditionalStyle[Any], None] = None


@dataclass(frozen=True)
class Table(Buildable, Generic[T]):
    columns: list[TableColumn[T]]
    data: list[T]
    column_name_style: Union[Style, None] = None
    data_style: Union[Style, None] = None

    @override
    def internal_build(self, context: BuildContext) -> None:
        for i, column in enumerate(self.columns):
            if column.width:
                context.collect_column_dimension(
                    ColumnDimension(context.column_index + i, column.width)
                )
        self.build().internal_build(context)

    @override
    def build(self) -> 'Buildable':
        return Column([
            Styler(
                Row(children=self.__get_column_name_cells()),
                self.column_name_style
            ),
            Styler(
                Row(children=self.__get_value_columns()),
                self.data_style
            )
        ])

    def __get_column_name_cells(self) -> list[Buildable]:
        excel_cells: list[Buildable] = []
        for column in self.columns:
            excel_cells.append(
                Styler(
                    ExcelCell(column.name),
                    column.column_name_style
                )
            )
        return excel_cells

    def __get_value_columns(self) -> list[Buildable]:
        columns: list[Buildable] = []
        for column in self.columns:
            excel_cells = []
            conditional_style_names: list[str] = []
            for model in self.data:
                conditional_style_index: Union[int, None] = None
                value = column.value(model)
                if column.conditional_style is not None and type(column.conditional_style) is ModelConditionalStyle:
                    conditional_style_index = column.conditional_style.selector(model)
                elif column.conditional_style is not None and type(column.conditional_style) is ValueConditionalStyle: 
                    conditional_style_index = column.conditional_style.selector(value)
                excel_cells.append(ExcelCell(value, conditional_style_index))
            columns.append(
                Styler(
                    ConditionalStyler(
                        Column(children=excel_cells),
                        column.conditional_style.styles if column.conditional_style is not None else [],
                        conditional_style_names
                    ),
                    column.value_style
                )
            )
        return columns
