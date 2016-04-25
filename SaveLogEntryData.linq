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
{	long last_working_id = 2777869;
	var batch_size = 1000;
	long last_id = 0;
	var filePath = "C:\\tmp\\logs.csv";
	
	if(!File.Exists(filePath))
		File.CreateText(filePath);
	
	if(File.ReadLines(filePath).Count() > 0)
	{
		var text = File.ReadLines(filePath).Last();
		try{
			var r =ParseRow(text);
			last_working_id = r.Item1 + 1;
		}
		catch(DataException)
		{
		}
	}
	last_id = LogEntries.OrderByDescending(x => x.Id).First().Id;
	
	while(last_working_id < last_id)
	{
		var tid  =  ProcessBatch((int) last_working_id + 1,(int) batch_size,filePath,true);
		if(tid == -1)
			last_working_id += batch_size;
		else
		{
			last_working_id = tid + 1;
			Debug.WriteLine(string.Format("Wrote up to id {0}",last_working_id));
		}
		
		
	}
	
}
public long ProcessBatch(int start, int size, string path, bool display = false)
{
	var q = LogEntries.Where( i => i.Id >= start && i.Id < start + size) ;
	var items = new List<Tuple<long,DateTime,long,string,string,string>>();
	var lastid = 0;
	q.ToList().ForEach(item => {
		var t = NewRow(item.Id,item.EntryTime,item.SeverityLevel, item.Username,item.Message,item.CallingMethodName);
		items.Add(t);
		
	});
	
	List<string> lines = new List<string>();
	items.ForEach(item => {lines.Add(item.ToString());});
	if (display)
		lines.Dump();
	File.AppendAllLines(path,lines.ToArray());
	if(items.Any())
		return items.Max( x => x.Item1);
	else return -1;
}

public static class Extensions
{
	public static string ToString(this Tuple<long,DateTime,long,string,string,string> data)
	{
		return string.Format("{0},{1}{2}{3}{4}{5}",data.Item1,data.Item2,data.Item3,data.Item4,data.Item5,data.Item5);
	}
	public static string JoinStrings<T>(
		this IEnumerable<T> values, string separator)
	{
		var stringValues = values.Select(item =>
			(item == null ? string.Empty : item.ToString()));
		return string.Join(separator, stringValues.ToArray());
	}
}
public Tuple<long,DateTime,long,string,string,string> NewRow()
{
	return new Tuple<long,DateTime,long,string,string,string>(0,DateTime.Now,0,string.Empty,string.Empty,string.Empty);
}
public Tuple<long,DateTime,long,string,string,string> NewRow(long id, DateTime dt, long severity,string user,string message, string method)
{
	return new Tuple<long,DateTime,long,string,string,string>(id,dt,severity,user,message,method);
}
public Tuple<long,DateTime,long,string,string,string> ParseRow(string row)
{
	var sItems = row.Split(',');
	if(sItems.Count() == 6)
	{
		long id,severity;
		DateTime dt;
		var idOk=long.TryParse(sItems[0].Replace("(",""), out id);
		var dtOK = DateTime.TryParse(sItems[1], out dt);
		var severityOK = long.TryParse(sItems[2], out severity);
		
		var t = NewRow(id,dt,severity,sItems[3],sItems[4],sItems[5]);
		return t;
		
	}
	else
		throw new DataException();
}

// Define other methods and classes here