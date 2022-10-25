import pm4py as pm
import os
from pathlib import Path
from pm4py.objects.petri_net.utils import petri_utils
initial_markings, final_markings = [], []

def extract_list(lpm_field):
    lpm_list = lpm_field.split('+')[1:-1]
    lpm_list = map(lambda item: int(item[4:]), lpm_list)
    return list(lpm_list)
    
def prev_transitions(net, transition):
    # searching places source from None transition
    for arc in list(transition.in_arcs):
        # searching all transitions in from the current place
        place = arc.source
        for arc in list(place.in_arcs):
            source = arc.source
            # if source transition is not None, appending to list of final markings
            if source.label != None:
                final_markings.append(source.label)
            else:
                # recursion with same net without the current place
                net = petri_utils.remove_place(net, place)
                prev_transitions(net, source)

def next_transitions(net, transition):
    # searching places target from None transition
    for arc in list(transition.out_arcs):
            place = arc.target
            # searching all transitions out from the current place
            for arc in list(place.out_arcs):
                target = arc.target
                # if target transition is not None, appending to list of initial markings
                if target.label != None:
                    initial_markings.append(target.label)
                else:
                    # recursion with same net without the current place
                    net = petri_utils.remove_place(net, place)
                    next_transitions(net, target)

def extract_initial_final_markings(input_lpms, num):
        # there are two nets, because recursion for initial_markings delete places,
        # so we risk that results of final_markings are influenced by the previous

        prev_net, initial_marking, final_marking = pm.read_pnml(input_lpms+"testLaura_"+str(num)+".pnml")
        next_net, initial_marking, final_marking = pm.read_pnml(input_lpms+"testLaura_"+str(num)+".pnml")
        """
        # Nei nostri test gli lpm partono da 1, mentre in quelli della prof partono da 0
        prev_net, initial_marking, final_marking = pm.read_pnml(input_lpms+"testLaura_"+str(num-1)+".pnml")
        next_net, initial_marking, final_marking = pm.read_pnml(input_lpms+"testLaura_"+str(num-1)+".pnml")
        """
        
        pm.view_petri_net(prev_net, initial_marking, final_marking)
        
        #setting initial and final places
        initial_place, final_place = None, None
        for place in prev_net.places:
            if place.name == 'n1': initial_place = place 
            if place.name == 'n2': final_place = place 
        
        #iterating on arcs' net, here we can iterate over net1 or net2, no differences
        for arc in list(next_net.arcs):
            source, target = arc.source, arc.target
            
            #checking if the place is the initial
            if source.name == initial_place.name:
                # if label target is None, must check next transitions
                if target.label != None:
                    initial_markings.append(target.label)
                else:
                    #recursion whit net1
                    next_transitions(next_net, target)

            #checking if the place is the final
            if target.name == final_place.name:
                # if label source is None, must check previous transitions
                if source.label != None:
                    final_markings.append(source.label)
                else:
                    #recursion whit net2
                    prev_transitions(prev_net, source)
        
        """
        for arc in initial_place.out_arcs:
            target = arc.target
            if target.label != None:
                initial_markings.append(target.label)
            else:
                next_transitions(next_net, target)

        for arc in final_place.in_arcs:
            source = arc.source
            if source.label != None:
                final_markings.append(source.label)
            else:
                prev_transitions(prev_net, source)
        """
        ordered_initial_markings = sorted(initial_markings)
        ordered_final_markings = sorted(final_markings)
        return ordered_initial_markings, ordered_final_markings

def compression(input_xes, input_lpms, limit, out_xes):
    """
    Count number of occurrences in xes file, and each time that LPM appears, increasing relative index
    on the list
    """
    # reading xes file
    file_xes = pm.read_xes(input_xes)

    # extracting number of files contained in the LPMs folder
    number_lpms_files = len([name for name in os.listdir(input_lpms) if os.path.isfile(os.path.join(input_lpms, name))])

    # define a list that contains as many zeros as there are LPMs
    count_list = [0 for i in range(number_lpms_files)]

    # calculating most frequent index of LPMs
    iteration = 0
    while(iteration < limit):
        for trace in file_xes:
            for event in trace:
                # getting LPM values as "[v1, ..., vN]"
                lpms_event_string = event._dict["LPMs_list"]
                
                # converting list in [v1, ..., vN]
                lpms_event_list = extract_list(lpms_event_string)
                
                # iterating on list values
                for lpm in lpms_event_list:
                    # in the algorythm LPMs start from one, while in the list from zero
                    count_list[lpm] += 1
                    
                    """
                    Nei nostri test gli lpm partono da 1
                    count_list[lpm-1] += 1
                    """

        # most frequent index of LPMs
        """
        # nei nostri test gli lpm partono da 1
        max_index = count_list.index(max(count_list)) +1
        """
        max_index = count_list.index(max(count_list))

        print(count_list)
        print("Max index in lpm: "+str(max_index))

        initial_markings, final_markings = extract_initial_final_markings(input_lpms, max_index)

        """
        Having found the LPMS that compresses the most, one modifies the xes by scrolling through the traces, and for each event,
        you check whether the index to be deleted appears in the LPMs attribute; if so,
        if the event is the first in the trace, the name is modified, otherwise the
        the event itself
        """
        for trace in file_xes:
            # index represents the index of the event on which it is iterating
            index = 0

            new_trace = True
            prev = None

            while(index < len(trace)):
                # setting the current event
                event = trace[index]
                # setting the next event equal to the current +1
                next = trace[index+1] if index<len(trace)-1 else None

                # we get the value of LPMs in the form of "[v1, ..., vN]"
                lpms_event_string = event._dict["LPMs_list"]
                
                # we convert to list of numeric values [v1, ..., vN]
                lpms_event_list = extract_list(lpms_event_string)
                
                # if the index that appears multiple times is contained in the current lpm 
                if(max_index in lpms_event_list):
                
                    # if the the current event name appears in final markings,
                    # and the next exists, and its name appears in initial markings,
                    # new trace is starting
                    if(next
                    and event._dict["concept:name"] in final_markings
                    and next._dict["concept:name"] in initial_markings):
                        new_trace = True
                    
                    # if a previous event exists, and its name is equal to the current event,
                    # and the initial_markings is equal to the final markings, it means
                    # that it's a loop, so a new trace is must start
                    if(prev
                    and prev == event._dict["concept:name"]
                    and initial_markings == final_markings):
                        new_trace = True

                    # setting the previous event equal to the current one
                    prev = event._dict["concept:name"]

                    # event name is replaced, otherwise the event itself is deleted.
                    if(not new_trace):
                        # you delete the event
                        del trace._list[index]
                    else:
                        new_trace = False
                        # you replace the name and delete the list of lpm.
                        event._dict['concept:name'] = 'LPM'+str(max_index)+'Iteration:'+str(iteration)
                        
                        #scommentare, commentato per test nostro
                        #del event._dict["LPMs_list"]
                        
                        del event._dict["LPMs_binary"]
                        del event._dict["LPMs_frequency"]
                        
                        # is incremented to iterate on the next event
                        index += 1
                else:
                    # if the index of the most frequent does not appear in the list of lpms.
                    # you delete the list of lpms.
                    
                    #scommentare, commentato per test nostro
                    #del event._dict["LPMs_list"]
                    
                    del event._dict["LPMs_binary"]
                    del event._dict["LPMs_frequency"]
                    new_trace = True
                    
                    # must be none here
                    prev = None
                    
                    # is incremented to iterate on the next event
                    index += 1
        iteration += 1

    # overwrite file if already exists
    if Path(out_xes).exists():
        Path.unlink(Path(out_xes))
    pm.write_xes(file_xes, out_xes)