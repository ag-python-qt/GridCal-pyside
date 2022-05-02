# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'banner.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from .icons_rc import *

class Ui_splashScreen(object):
    def setupUi(self, splashScreen):
        if not splashScreen.objectName():
            splashScreen.setObjectName(u"splashScreen")
        splashScreen.resize(570, 354)
        splashScreen.setBaseSize(QSize(0, 0))
        icon = QIcon()
        icon.addFile(u":/Program icon/GridCal_icon.svg", QSize(), QIcon.Normal, QIcon.Off)
        splashScreen.setWindowIcon(icon)
        splashScreen.setIconSize(QSize(24, 24))
        splashScreen.setDocumentMode(False)
        splashScreen.setTabShape(QTabWidget.Rounded)
        splashScreen.setUnifiedTitleAndToolBarOnMac(False)
        self.actionOpen_file = QAction(splashScreen)
        self.actionOpen_file.setObjectName(u"actionOpen_file")
        icon1 = QIcon()
        icon1.addFile(u":/Icons/icons/loadc.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOpen_file.setIcon(icon1)
        self.actionSave = QAction(splashScreen)
        self.actionSave.setObjectName(u"actionSave")
        icon2 = QIcon()
        icon2.addFile(u":/Icons/icons/savec.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSave.setIcon(icon2)
        self.actionExport = QAction(splashScreen)
        self.actionExport.setObjectName(u"actionExport")
        icon3 = QIcon()
        icon3.addFile(u":/Icons/icons/save.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionExport.setIcon(icon3)
        self.actionNew_project = QAction(splashScreen)
        self.actionNew_project.setObjectName(u"actionNew_project")
        icon4 = QIcon()
        icon4.addFile(u":/Icons/icons/new2c.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionNew_project.setIcon(icon4)
        self.actionPower_flow = QAction(splashScreen)
        self.actionPower_flow.setObjectName(u"actionPower_flow")
        icon5 = QIcon()
        icon5.addFile(u":/Icons/icons/pf.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionPower_flow.setIcon(icon5)
        self.actionPower_Flow_Time_series = QAction(splashScreen)
        self.actionPower_Flow_Time_series.setObjectName(u"actionPower_Flow_Time_series")
        icon6 = QIcon()
        icon6.addFile(u":/Icons/icons/pf_ts.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionPower_Flow_Time_series.setIcon(icon6)
        self.actionBigger_nodes = QAction(splashScreen)
        self.actionBigger_nodes.setObjectName(u"actionBigger_nodes")
        icon7 = QIcon()
        icon7.addFile(u":/Icons/icons/plus (gray).svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionBigger_nodes.setIcon(icon7)
        self.actionSmaller_nodes = QAction(splashScreen)
        self.actionSmaller_nodes.setObjectName(u"actionSmaller_nodes")
        icon8 = QIcon()
        icon8.addFile(u":/Icons/icons/minus (gray).svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSmaller_nodes.setIcon(icon8)
        self.actionPower_flow_Stochastic = QAction(splashScreen)
        self.actionPower_flow_Stochastic.setObjectName(u"actionPower_flow_Stochastic")
        icon9 = QIcon()
        icon9.addFile(u":/Icons/icons/stochastic_power_flow.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionPower_flow_Stochastic.setIcon(icon9)
        self.actionVoltage_stability = QAction(splashScreen)
        self.actionVoltage_stability.setObjectName(u"actionVoltage_stability")
        icon10 = QIcon()
        icon10.addFile(u":/Icons/icons/continuation_power_flow.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionVoltage_stability.setIcon(icon10)
        self.actionAbout = QAction(splashScreen)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionAbout.setIcon(icon)
        self.actionCenter_view = QAction(splashScreen)
        self.actionCenter_view.setObjectName(u"actionCenter_view")
        icon11 = QIcon()
        icon11.addFile(u":/Icons/icons/resize.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionCenter_view.setIcon(icon11)
        self.actionShort_Circuit = QAction(splashScreen)
        self.actionShort_Circuit.setObjectName(u"actionShort_Circuit")
        icon12 = QIcon()
        icon12.addFile(u":/Icons/icons/short_circuit.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionShort_Circuit.setIcon(icon12)
        self.actionAutoatic_layout = QAction(splashScreen)
        self.actionAutoatic_layout.setObjectName(u"actionAutoatic_layout")
        icon13 = QIcon()
        icon13.addFile(u":/Icons/icons/automatic_layout.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionAutoatic_layout.setIcon(icon13)
        self.actionLatin_Hypercube_Sampling = QAction(splashScreen)
        self.actionLatin_Hypercube_Sampling.setObjectName(u"actionLatin_Hypercube_Sampling")
        icon14 = QIcon()
        icon14.addFile(u":/Icons/icons/latin_hypercube2.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionLatin_Hypercube_Sampling.setIcon(icon14)
        self.actionBlackout_cascade = QAction(splashScreen)
        self.actionBlackout_cascade.setObjectName(u"actionBlackout_cascade")
        self.actionBlackout_cascade.setCheckable(True)
        icon15 = QIcon()
        icon15.addFile(u":/Icons/icons/blackout.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionBlackout_cascade.setIcon(icon15)
        self.actionOPF = QAction(splashScreen)
        self.actionOPF.setObjectName(u"actionOPF")
        icon16 = QIcon()
        icon16.addFile(u":/Icons/icons/dcopf.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOPF.setIcon(icon16)
        self.actionOPF_time_series = QAction(splashScreen)
        self.actionOPF_time_series.setObjectName(u"actionOPF_time_series")
        icon17 = QIcon()
        icon17.addFile(u":/Icons/icons/dcopf_ts.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOPF_time_series.setIcon(icon17)
        self.actionDetect_transformers = QAction(splashScreen)
        self.actionDetect_transformers.setObjectName(u"actionDetect_transformers")
        icon18 = QIcon()
        icon18.addFile(u":/Icons/icons/detect_tr.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionDetect_transformers.setIcon(icon18)
        self.actionAuto_rate_branches = QAction(splashScreen)
        self.actionAuto_rate_branches.setObjectName(u"actionAuto_rate_branches")
        icon19 = QIcon()
        icon19.addFile(u":/Icons/icons/rate_br.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionAuto_rate_branches.setIcon(icon19)
        self.actionExport_all_the_device_s_profiles = QAction(splashScreen)
        self.actionExport_all_the_device_s_profiles.setObjectName(u"actionExport_all_the_device_s_profiles")
        self.actionExport_all_the_device_s_profiles.setIcon(icon3)
        self.actionGrid_Reduction = QAction(splashScreen)
        self.actionGrid_Reduction.setObjectName(u"actionGrid_Reduction")
        icon20 = QIcon()
        icon20.addFile(u":/Icons/icons/grid_reduction.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionGrid_Reduction.setIcon(icon20)
        self.actionStorage_location_suggestion = QAction(splashScreen)
        self.actionStorage_location_suggestion.setObjectName(u"actionStorage_location_suggestion")
        self.actionStorage_location_suggestion.setCheckable(True)
        icon21 = QIcon()
        icon21.addFile(u":/Icons/icons/storage_loc.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionStorage_location_suggestion.setIcon(icon21)
        self.actionLaunch_data_analysis_tool = QAction(splashScreen)
        self.actionLaunch_data_analysis_tool.setObjectName(u"actionLaunch_data_analysis_tool")
        icon22 = QIcon()
        icon22.addFile(u":/Icons/icons/bars.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionLaunch_data_analysis_tool.setIcon(icon22)
        self.actionOnline_documentation = QAction(splashScreen)
        self.actionOnline_documentation.setObjectName(u"actionOnline_documentation")
        icon23 = QIcon()
        icon23.addFile(u":/Icons/icons/new.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOnline_documentation.setIcon(icon23)
        self.actionExport_all_results = QAction(splashScreen)
        self.actionExport_all_results.setObjectName(u"actionExport_all_results")
        icon24 = QIcon()
        icon24.addFile(u":/Icons/icons/export_pickle.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionExport_all_results.setIcon(icon24)
        self.actionSave_as = QAction(splashScreen)
        self.actionSave_as.setObjectName(u"actionSave_as")
        self.actionSave_as.setIcon(icon3)
        self.actionDelete_selected = QAction(splashScreen)
        self.actionDelete_selected.setObjectName(u"actionDelete_selected")
        icon25 = QIcon()
        icon25.addFile(u":/Icons/icons/delete3.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionDelete_selected.setIcon(icon25)
        self.actionPTDF = QAction(splashScreen)
        self.actionPTDF.setObjectName(u"actionPTDF")
        icon26 = QIcon()
        icon26.addFile(u":/Icons/icons/ptdf.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionPTDF.setIcon(icon26)
        self.actionOTDF = QAction(splashScreen)
        self.actionOTDF.setObjectName(u"actionOTDF")
        icon27 = QIcon()
        icon27.addFile(u":/Icons/icons/otdf.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOTDF.setIcon(icon27)
        self.actionReset_console = QAction(splashScreen)
        self.actionReset_console.setObjectName(u"actionReset_console")
        icon28 = QIcon()
        icon28.addFile(u":/Icons/icons/undo.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionReset_console.setIcon(icon28)
        self.actionOpf_to_Power_flow = QAction(splashScreen)
        self.actionOpf_to_Power_flow.setObjectName(u"actionOpf_to_Power_flow")
        self.actionOpf_to_Power_flow.setCheckable(True)
        icon29 = QIcon()
        icon29.addFile(u":/Icons/icons/dcopf2ts.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOpf_to_Power_flow.setIcon(icon29)
        self.actionTry_to_fix_buses_location = QAction(splashScreen)
        self.actionTry_to_fix_buses_location.setObjectName(u"actionTry_to_fix_buses_location")
        icon30 = QIcon()
        icon30.addFile(u":/Icons/icons/move_bus.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionTry_to_fix_buses_location.setIcon(icon30)
        self.actionSet_OPF_generation_to_profiles = QAction(splashScreen)
        self.actionSet_OPF_generation_to_profiles.setObjectName(u"actionSet_OPF_generation_to_profiles")
        self.actionSet_OPF_generation_to_profiles.setIcon(icon29)
        self.actionPTDF_time_series = QAction(splashScreen)
        self.actionPTDF_time_series.setObjectName(u"actionPTDF_time_series")
        icon31 = QIcon()
        icon31.addFile(u":/Icons/icons/ptdf_ts.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionPTDF_time_series.setIcon(icon31)
        self.actionShow_color_controls = QAction(splashScreen)
        self.actionShow_color_controls.setObjectName(u"actionShow_color_controls")
        self.actionShow_color_controls.setCheckable(True)
        icon32 = QIcon()
        icon32.addFile(u":/Icons/icons/map.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionShow_color_controls.setIcon(icon32)
        self.actionAdd_circuit = QAction(splashScreen)
        self.actionAdd_circuit.setObjectName(u"actionAdd_circuit")
        icon33 = QIcon()
        icon33.addFile(u":/Icons/icons/load_add.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionAdd_circuit.setIcon(icon33)
        self.actionSync = QAction(splashScreen)
        self.actionSync.setObjectName(u"actionSync")
        self.actionSync.setCheckable(True)
        icon34 = QIcon()
        icon34.addFile(u":/Icons/icons/sync.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSync.setIcon(icon34)
        self.actionDrawSchematic = QAction(splashScreen)
        self.actionDrawSchematic.setObjectName(u"actionDrawSchematic")
        icon35 = QIcon()
        icon35.addFile(u":/Icons/icons/grid_icon.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionDrawSchematic.setIcon(icon35)
        self.actionSigma_analysis = QAction(splashScreen)
        self.actionSigma_analysis.setObjectName(u"actionSigma_analysis")
        icon36 = QIcon()
        icon36.addFile(u":/Icons/icons/sigma.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSigma_analysis.setIcon(icon36)
        self.actionClear_stuff_running_right_now = QAction(splashScreen)
        self.actionClear_stuff_running_right_now.setObjectName(u"actionClear_stuff_running_right_now")
        icon37 = QIcon()
        icon37.addFile(u":/Icons/icons/clear_runs.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionClear_stuff_running_right_now.setIcon(icon37)
        self.actionAdd_default_catalogue = QAction(splashScreen)
        self.actionAdd_default_catalogue.setObjectName(u"actionAdd_default_catalogue")
        icon38 = QIcon()
        icon38.addFile(u":/Icons/icons/CatalogueAdd.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionAdd_default_catalogue.setIcon(icon38)
        self.actionFind_node_groups = QAction(splashScreen)
        self.actionFind_node_groups.setObjectName(u"actionFind_node_groups")
        self.actionFind_node_groups.setCheckable(True)
        icon39 = QIcon()
        icon39.addFile(u":/Icons/icons/color_grid2.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionFind_node_groups.setIcon(icon39)
        self.actiongrid_Generator = QAction(splashScreen)
        self.actiongrid_Generator.setObjectName(u"actiongrid_Generator")
        self.actiongrid_Generator.setIcon(icon13)
        self.centralwidget = QWidget(splashScreen)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setTextFormat(Qt.PlainText)
        self.label.setPixmap(QPixmap(u"../../../../pics/Promo 4.0.svg"))
        self.label.setScaledContents(True)

        self.verticalLayout.addWidget(self.label)

        splashScreen.setCentralWidget(self.centralwidget)

        self.retranslateUi(splashScreen)

        QMetaObject.connectSlotsByName(splashScreen)
    # setupUi

    def retranslateUi(self, splashScreen):
        splashScreen.setWindowTitle(QCoreApplication.translate("splashScreen", u"GridCal", None))
        self.actionOpen_file.setText(QCoreApplication.translate("splashScreen", u"Open file", None))
#if QT_CONFIG(shortcut)
        self.actionOpen_file.setShortcut(QCoreApplication.translate("splashScreen", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave.setText(QCoreApplication.translate("splashScreen", u"Save", None))
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("splashScreen", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionExport.setText(QCoreApplication.translate("splashScreen", u"Export schematic picture", None))
        self.actionNew_project.setText(QCoreApplication.translate("splashScreen", u"New project", None))
#if QT_CONFIG(shortcut)
        self.actionNew_project.setShortcut(QCoreApplication.translate("splashScreen", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.actionPower_flow.setText(QCoreApplication.translate("splashScreen", u"Power Flow", None))
#if QT_CONFIG(shortcut)
        self.actionPower_flow.setShortcut(QCoreApplication.translate("splashScreen", u"F5", None))
#endif // QT_CONFIG(shortcut)
        self.actionPower_Flow_Time_series.setText(QCoreApplication.translate("splashScreen", u"Power Flow: Time series", None))
#if QT_CONFIG(tooltip)
        self.actionPower_Flow_Time_series.setToolTip(QCoreApplication.translate("splashScreen", u"Power flow time series", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionPower_Flow_Time_series.setShortcut(QCoreApplication.translate("splashScreen", u"F6", None))
#endif // QT_CONFIG(shortcut)
        self.actionBigger_nodes.setText(QCoreApplication.translate("splashScreen", u"Expand", None))
#if QT_CONFIG(tooltip)
        self.actionBigger_nodes.setToolTip(QCoreApplication.translate("splashScreen", u"Expand distances", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionBigger_nodes.setShortcut(QCoreApplication.translate("splashScreen", u"F3", None))
#endif // QT_CONFIG(shortcut)
        self.actionSmaller_nodes.setText(QCoreApplication.translate("splashScreen", u"Shrink", None))
#if QT_CONFIG(tooltip)
        self.actionSmaller_nodes.setToolTip(QCoreApplication.translate("splashScreen", u"Shrink distances", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionSmaller_nodes.setShortcut(QCoreApplication.translate("splashScreen", u"F2", None))
#endif // QT_CONFIG(shortcut)
        self.actionPower_flow_Stochastic.setText(QCoreApplication.translate("splashScreen", u"Stochastic power flow: Monte Carlo", None))
#if QT_CONFIG(tooltip)
        self.actionPower_flow_Stochastic.setToolTip(QCoreApplication.translate("splashScreen", u"Monte Carlo stochastic power flow", None))
#endif // QT_CONFIG(tooltip)
        self.actionVoltage_stability.setText(QCoreApplication.translate("splashScreen", u"Continuation power flow", None))
#if QT_CONFIG(tooltip)
        self.actionVoltage_stability.setToolTip(QCoreApplication.translate("splashScreen", u"Continuation power flow", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionVoltage_stability.setShortcut(QCoreApplication.translate("splashScreen", u"F7", None))
#endif // QT_CONFIG(shortcut)
        self.actionAbout.setText(QCoreApplication.translate("splashScreen", u"About", None))
        self.actionCenter_view.setText(QCoreApplication.translate("splashScreen", u"center view", None))
#if QT_CONFIG(tooltip)
        self.actionCenter_view.setToolTip(QCoreApplication.translate("splashScreen", u"Center view", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionCenter_view.setShortcut(QCoreApplication.translate("splashScreen", u"F4", None))
#endif // QT_CONFIG(shortcut)
        self.actionShort_Circuit.setText(QCoreApplication.translate("splashScreen", u"Short Circuit", None))
        self.actionAutoatic_layout.setText(QCoreApplication.translate("splashScreen", u"Automatic grid layout", None))
#if QT_CONFIG(tooltip)
        self.actionAutoatic_layout.setToolTip(QCoreApplication.translate("splashScreen", u"Automatic layout the of the grid", None))
#endif // QT_CONFIG(tooltip)
        self.actionLatin_Hypercube_Sampling.setText(QCoreApplication.translate("splashScreen", u"Stochastic power flow: Latin Hypercube", None))
#if QT_CONFIG(tooltip)
        self.actionLatin_Hypercube_Sampling.setToolTip(QCoreApplication.translate("splashScreen", u"Latin Hypercube stochastic power flow", None))
#endif // QT_CONFIG(tooltip)
        self.actionBlackout_cascade.setText(QCoreApplication.translate("splashScreen", u"Blackout cascade", None))
#if QT_CONFIG(tooltip)
        self.actionBlackout_cascade.setToolTip(QCoreApplication.translate("splashScreen", u"Run a simulation or step by step blackout cascade", None))
#endif // QT_CONFIG(tooltip)
        self.actionOPF.setText(QCoreApplication.translate("splashScreen", u"OPF", None))
#if QT_CONFIG(tooltip)
        self.actionOPF.setToolTip(QCoreApplication.translate("splashScreen", u"Optimal power flow", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionOPF.setShortcut(QCoreApplication.translate("splashScreen", u"F9", None))
#endif // QT_CONFIG(shortcut)
        self.actionOPF_time_series.setText(QCoreApplication.translate("splashScreen", u"OPF time series", None))
#if QT_CONFIG(tooltip)
        self.actionOPF_time_series.setToolTip(QCoreApplication.translate("splashScreen", u"Optimal power flow time series", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionOPF_time_series.setShortcut(QCoreApplication.translate("splashScreen", u"F10", None))
#endif // QT_CONFIG(shortcut)
        self.actionDetect_transformers.setText(QCoreApplication.translate("splashScreen", u"Detect transformers", None))
#if QT_CONFIG(tooltip)
        self.actionDetect_transformers.setToolTip(QCoreApplication.translate("splashScreen", u"<html><head/><body><p>Detect transformers.</p><p>Use the nodes nominal voltage to determine which branches should be a transformer.</p><p>If a branch joins two nodes with different voltage levels, the branch should be a transformer.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.actionAuto_rate_branches.setText(QCoreApplication.translate("splashScreen", u"Auto rate branches", None))
#if QT_CONFIG(tooltip)
        self.actionAuto_rate_branches.setToolTip(QCoreApplication.translate("splashScreen", u"<html><head/><body><p>Automatic rating of the branches.</p><p>Use the branches calculated power to establish a rate, if the branch rate is unknown. A factor is available in the settings.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.actionExport_all_the_device_s_profiles.setText(QCoreApplication.translate("splashScreen", u"Export all the device's profiles", None))
        self.actionGrid_Reduction.setText(QCoreApplication.translate("splashScreen", u"Grid Reduction", None))
#if QT_CONFIG(tooltip)
        self.actionGrid_Reduction.setToolTip(QCoreApplication.translate("splashScreen", u"Performs a topological grid reduction", None))
#endif // QT_CONFIG(tooltip)
        self.actionStorage_location_suggestion.setText(QCoreApplication.translate("splashScreen", u"Storage location suggestion", None))
#if QT_CONFIG(tooltip)
        self.actionStorage_location_suggestion.setToolTip(QCoreApplication.translate("splashScreen", u"Suggest places where storage devices are useful", None))
#endif // QT_CONFIG(tooltip)
        self.actionLaunch_data_analysis_tool.setText(QCoreApplication.translate("splashScreen", u"Launch data analysis tool", None))
#if QT_CONFIG(shortcut)
        self.actionLaunch_data_analysis_tool.setShortcut(QCoreApplication.translate("splashScreen", u"F8", None))
#endif // QT_CONFIG(shortcut)
        self.actionOnline_documentation.setText(QCoreApplication.translate("splashScreen", u"Online documentation", None))
#if QT_CONFIG(shortcut)
        self.actionOnline_documentation.setShortcut(QCoreApplication.translate("splashScreen", u"F1", None))
#endif // QT_CONFIG(shortcut)
        self.actionExport_all_results.setText(QCoreApplication.translate("splashScreen", u"Export all results", None))
#if QT_CONFIG(tooltip)
        self.actionExport_all_results.setToolTip(QCoreApplication.translate("splashScreen", u"Export all the results", None))
#endif // QT_CONFIG(tooltip)
        self.actionSave_as.setText(QCoreApplication.translate("splashScreen", u"Save as", None))
        self.actionDelete_selected.setText(QCoreApplication.translate("splashScreen", u"Delete selected", None))
#if QT_CONFIG(tooltip)
        self.actionDelete_selected.setToolTip(QCoreApplication.translate("splashScreen", u"Delete selected objects", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionDelete_selected.setShortcut(QCoreApplication.translate("splashScreen", u"Del", None))
#endif // QT_CONFIG(shortcut)
        self.actionPTDF.setText(QCoreApplication.translate("splashScreen", u"PTDF (Power Transfer Distribution Factors)", None))
#if QT_CONFIG(tooltip)
        self.actionPTDF.setToolTip(QCoreApplication.translate("splashScreen", u"Power Transfer Distribution Factors", None))
#endif // QT_CONFIG(tooltip)
        self.actionOTDF.setText(QCoreApplication.translate("splashScreen", u"N-1 / OTDF (Outage Transfer Distribution Factors)", None))
#if QT_CONFIG(tooltip)
        self.actionOTDF.setToolTip(QCoreApplication.translate("splashScreen", u"N-1 / OTDF (Outage Transfer Distribution Factors)", None))
#endif // QT_CONFIG(tooltip)
        self.actionReset_console.setText(QCoreApplication.translate("splashScreen", u"Reset console", None))
        self.actionOpf_to_Power_flow.setText(QCoreApplication.translate("splashScreen", u"Set OPF results to Power flow (non destructive)", None))
#if QT_CONFIG(tooltip)
        self.actionOpf_to_Power_flow.setToolTip(QCoreApplication.translate("splashScreen", u"Set the OPF resultsinto the power flow or time series simulations (non destructive)", None))
#endif // QT_CONFIG(tooltip)
        self.actionTry_to_fix_buses_location.setText(QCoreApplication.translate("splashScreen", u"Correct buses location", None))
#if QT_CONFIG(tooltip)
        self.actionTry_to_fix_buses_location.setToolTip(QCoreApplication.translate("splashScreen", u"Set selected buses location closer to their neighbours", None))
#endif // QT_CONFIG(tooltip)
        self.actionSet_OPF_generation_to_profiles.setText(QCoreApplication.translate("splashScreen", u"Copy OPF generation to profiles (destructive)", None))
#if QT_CONFIG(tooltip)
        self.actionSet_OPF_generation_to_profiles.setToolTip(QCoreApplication.translate("splashScreen", u"Destructive copy of the OPF generation results to the input profiles", None))
#endif // QT_CONFIG(tooltip)
        self.actionPTDF_time_series.setText(QCoreApplication.translate("splashScreen", u"PTDF time series power flow", None))
#if QT_CONFIG(tooltip)
        self.actionPTDF_time_series.setToolTip(QCoreApplication.translate("splashScreen", u"Runs the PTDF based time series power flow", None))
#endif // QT_CONFIG(tooltip)
        self.actionShow_color_controls.setText(QCoreApplication.translate("splashScreen", u"Show color controls", None))
        self.actionAdd_circuit.setText(QCoreApplication.translate("splashScreen", u"Add circuit", None))
#if QT_CONFIG(tooltip)
        self.actionAdd_circuit.setToolTip(QCoreApplication.translate("splashScreen", u"Add circuit to the current circuit", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionAdd_circuit.setShortcut(QCoreApplication.translate("splashScreen", u"Ctrl+N, Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionSync.setText(QCoreApplication.translate("splashScreen", u"Sync", None))
#if QT_CONFIG(tooltip)
        self.actionSync.setToolTip(QCoreApplication.translate("splashScreen", u"Sync with the file for colaborative editing of the grid", None))
#endif // QT_CONFIG(tooltip)
        self.actionDrawSchematic.setText(QCoreApplication.translate("splashScreen", u"Draw schematic", None))
        self.actionSigma_analysis.setText(QCoreApplication.translate("splashScreen", u"Sigma analysis", None))
#if QT_CONFIG(tooltip)
        self.actionSigma_analysis.setToolTip(QCoreApplication.translate("splashScreen", u"Perform HELM-Sigma analysis", None))
#endif // QT_CONFIG(tooltip)
        self.actionClear_stuff_running_right_now.setText(QCoreApplication.translate("splashScreen", u"Clear \"stuff running right now\"", None))
        self.actionAdd_default_catalogue.setText(QCoreApplication.translate("splashScreen", u"Add default catalogue", None))
        self.actionFind_node_groups.setText(QCoreApplication.translate("splashScreen", u"Find node groups", None))
#if QT_CONFIG(tooltip)
        self.actionFind_node_groups.setToolTip(QCoreApplication.translate("splashScreen", u"<html><head/><body><p>Finds the electrically related nodes by using their electrical distance and the DBSCAN clustering method</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.actiongrid_Generator.setText(QCoreApplication.translate("splashScreen", u"Grid Generator", None))
#if QT_CONFIG(shortcut)
        self.actiongrid_Generator.setShortcut(QCoreApplication.translate("splashScreen", u"Ctrl+G", None))
#endif // QT_CONFIG(shortcut)
        self.label.setText("")
    # retranslateUi

