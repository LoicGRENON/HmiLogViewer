# HmiLogViewer

HmiLogViewer is a tool for viewing log data created into Schneider Electric Magelis HMI touch panel (but may probably be used for another touch panel type).
Log data is stored in a CSV file.
Each row of the csv file is formatted in 3 tab separated fields : Date / Time / Message
The "Message" field contains log data and each data value are separated by a semi-colon.
The content and the type of data values are configured on a YAML config file.
