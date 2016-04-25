<Query Kind="Program">
  <Connection>
    <ID>5b75d298-f4ec-40d2-b6c2-fb898847c144</ID>
    <Persist>true</Persist>
    <Server>devweb.gsbeng.local</Server>
    <SqlSecurity>true</SqlSecurity>
    <UserName>GSBSCM-Login</UserName>
    <Password>AQAAANCMnd8BFdERjHoAwE/Cl+sBAAAA7X5zEsU/50OZEIxDEj5zLwAAAAACAAAAAAADZgAAwAAAABAAAAC43ZCd4YfhEPG71TP6Ca0tAAAAAASAAACgAAAAEAAAAMGPTLJJ+1it57l5FJ2vW7gQAAAADRHVGTonAJEcpaeTQ/2A0hQAAABdynANAuiqOaB+ebjli9nsiWCN1g==</Password>
    <Database>GSBSCM</Database>
    <ShowServer>true</ShowServer>
  </Connection>
</Query>

void Main()
{
	var path = "C:\\Users\\Developer.TAPPINDEV\\BitTorrent Sync\\projects\\log-insight\\logs.csv";
	var cList = Connectors.ToList();
	var listLines = new List<string>();
	cList.ForEach(x => 
		{
			var sLine = string.Format("{0},{1},{2},{}",x.Id,x.Address,x.DisplayName,x.Certificate);
			listLines.Add(sLine);
			
		}
	);
	File.AppendAllLines(path,listLines);
	listLines.Count().Dump("Lines written to " + path);

}

// Define other methods and classes here
