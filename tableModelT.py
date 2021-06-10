from PySide2.QtCore import Qt, QModelIndex, QAbstractTableModel


class TableModel(QAbstractTableModel):
    def __init__(self, datas=None, parent=None):
        super(TableModel, self).__init__(parent)

        if datas is None:
            self.datas = []
        else:
            self.datas = datas

    def rowCount(self, index=QModelIndex()):
        """ Returns the number of rows the model holds. """
        return len(self.datas)

    def columnCount(self, index):
        """ Returns the number of columns the model holds. """
        return 7

    def data(self, index, role=Qt.DisplayRole):
        """ Depending on the index and role given, return data. If not
            returning data, return None (PySide equivalent of QT's
            "invalid QVariant").
        """
        if not index.isValid():
            return None

        if not 0 <= index.row() < len(self.datas):
            return None

        if role == Qt.DisplayRole:
            Temperature = self.datas[index.row()]["Temperature"]
            yCH4 = self.datas[index.row()]["yCH4"]
            yCO = self.datas[index.row()]["yCO"]
            yCO2 = self.datas[index.row()]["yCO2"]
            yH2 = self.datas[index.row()]["yH2"]
            yN2 = self.datas[index.row()]["yN2"]
            yH2O = self.datas[index.row()]["yH2O"]

            if index.column() == 0:
                return Temperature
            elif index.column() == 1:
                return yCH4
            elif index.column() == 2:
                return yCO
            elif index.column() == 3:
                return yCO2
            elif index.column() == 4:
                return yH2
            elif index.column() == 5:
                return yN2
            elif index.column() == 6:
                return yH2O

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """ Set the headers to be displayed. """
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section == 0:
                return "Temperature"
            elif section == 1:
                return "yCH4"
            elif section == 2:
                return "yCO"
            elif section == 3:
                return "yCO2"
            elif section == 4:
                return "yH2"
            elif section == 5:
                return "yN2"
            elif section == 6:
                return "yH2O"

        return None

    def insertRows(self, position, rows=1, index=QModelIndex()):
        """ Insert a row into the model. """
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)

        for row in range(rows):
            self.datas.insert(position + row,
                              {"Temperature": "", "yCH4": "", "yCO": "", "yCO2": "", "yH2": "", "yN2": "", "yH2O": ""})

        self.endInsertRows()
        return True

    def removeRows(self, position, rows=1, index=QModelIndex()):
        """ Remove a row from the model. """
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)

        del self.datas[position:position + rows]

        self.endRemoveRows()
        return True

    def setData(self, index, value, role=Qt.EditRole):
        """ Adjust the data (set it to <value>) depending on the given
            index and role.
        """
        if role != Qt.EditRole:
            return False

        if index.isValid() and 0 <= index.row() < len(self.datas):
            data = self.datas[index.row()]
            if index.column() == 0:
                data["Temperature"] = value
            elif index.column() == 1:
                data["yCH4"] = value
            elif index.column() == 2:
                data["yCO"] = value
            elif index.column() == 3:
                data["yCO2"] = value
            elif index.column() == 4:
                data["yH2"] = value
            elif index.column() == 5:
                data["yN2"] = value
            elif index.column() == 6:
                data["yH2O"] = value
            else:
                return False

            self.dataChanged.emit(index, index, 0)
            return True

        return False

    def flags(self, index):
        """ Set the item flags at the given index. Seems like we're
            implementing this function just to see how it's done, as we
            manually adjust each tableView to have NoEditTriggers.
        """
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index) |
                            Qt.ItemIsEditable)