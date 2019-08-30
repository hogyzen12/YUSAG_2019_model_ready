clear all
%programatically read if needed/
%Due to small data easier to load and save workspace
%read in YUSAG formatted sheet
%NCAAFCS_Results_reader('NCAA_FCS_Results_2017_.csv', 2, 0)
%NCAAFCSResults2017 = ans 
%read in Dictionary
%read_csvsheet('Dictionary.csv','1')
%Dictionary = ans

load('dictionaries.mat')
load('FBS_2017.mat')

input = FBS_2017

%looping through both columns read in with team abbreviations
for both = 1:2
%looping for all teams/games in the year reading
  for i = 1:size(input(:,both))
    %looping through the dictionary
    flag_dict = 0
    for j = 1:size(DictionaryFCS(:,2))
      %if abbreviation in game log is same as abbreviation in dictionary
      if (input(i,both) == DictionaryFCS(j,2)) 
        %Replace abbreviation in game log with full name
        input(i,both) = DictionaryFCS(j,1);
        flag_dict = 1
      end
    end
    for j = 1:size(DictionaryFBS(:,2))
      if (input(i,both) == DictionaryFBS(j,2)) 
        %Replace abbreviation in game log with full name
        input(i,both) = DictionaryFBS(j,1);
        flag_dict = 1
      end
    end
    for j = 1:size(DictionaryExclude(:,2))
      if (input(i,both) == DictionaryExclude(j,2)) 
        %Replace abbreviation in game log with full name
        input(i,both) = "0";
        flag_dict = 1
      end
    end
    if (flag_dict == 0)
      input(i,both) = "0";
    end
    end
  end

%export the updated array into a CSV sheet to allow for copy paste
%into the YUSAG formatted CSV sheet from which we read initial data
cell2csv("games_full_name_season.csv",input)