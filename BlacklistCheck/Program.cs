// See https://aka.ms/new-console-template for more information

using System.Net;
using NetTools;

const string workingDirectory = "./";

string[] ipBlacklistFiles = [
    workingDirectory + "userdata/blacklists/ipv4.txt",
    workingDirectory + "userdata/blacklists/vpn-or-datacenter-ipv4-ranges.txt"
];

const string vpnProviderIpAddresses = workingDirectory + "userdata/provider_ips.txt";
const string saveFile = workingDirectory + "userdata/not_banned_ips.txt";

List<string> vpnProviderIpList = [];  // Service IP addresses to check against a blacklist
List<string> blacklistedIpRanges = [];  // Blacklisted IP ranges
List<string> blacklistedProviderIps = [];
List<string> safeIpAddresses = [];  // End result, non blacklisted IP addresses

Console.WriteLine("Loading the lists");
foreach (var vpnIpStr in File.ReadLines(vpnProviderIpAddresses))
{
    vpnProviderIpList.Add(vpnIpStr.Trim());
}

foreach (var ipBlacklistFile in ipBlacklistFiles)
{
    foreach (var blacklistedIpRangeStr in File.ReadLines(ipBlacklistFile))
    {
        blacklistedIpRanges.Add(blacklistedIpRangeStr.Trim());
    }
}

List<string> blacklistedIpRangesNoDupes = blacklistedIpRanges.Distinct().ToList();

Console.WriteLine("Checking ips...");

foreach (var blacklistedIpRangeStr in blacklistedIpRangesNoDupes)
{
    var blacklistedIpRange = IPAddressRange.Parse(blacklistedIpRangeStr);
    foreach (var ipStr in vpnProviderIpList)
    {
        if (blacklistedIpRange.Contains(IPAddress.Parse(ipStr)))
        {
            blacklistedProviderIps.Add(ipStr);
        }
    }
}

Console.WriteLine("Exporting");
File.WriteAllLines(saveFile, vpnProviderIpList.Except(blacklistedProviderIps).ToList());

Console.WriteLine("Done");
