var editChanged = false;
var changedNodes = {};
function resetChanges() {
  for (var idx in changedNodes) {
    var node = changedNodes[idx];
    $(node).val($(node).attr('default-val'));
    delete changedNodes[idx];
  }
}

$(function() {
  /* activate tooltip */
  $('a[rel=tooltip]').tooltip();
  /* edit answer */
  $('.edit-field').change(function() {
    var def = $(this).attr('default-val');
    var val = $(this).val();
    if (def !== val) {
      editChanged = true;
      changedNodes[$(this).attr('question-id')] = $(this);
    } else {
      delete changedNodes[$(this).attr('question-id')];
      editChanged = false;
    }
  });
  $('.close-modal').click(function() {
    if (editChanged) {
      if (confirm('変更があります。変更を破棄してもいいですか？')) {
        resetChanges();
        editChanged = false;
        $(this).parents('.modal').modal('hide');
      }
    } else {
      $(this).parents('.modal').modal('hide');
    }
  });
  $('.edit-submit').click(function() {
    var parentModal = $(this).parents('.modal');
    if ($.isEmptyObject(changedNodes)) {
      alert('何も変更されていません。');
    } else {
      var ns = [];
      for (var idx in changedNodes) {
        ns.push({qid: idx, value: $(changedNodes[idx]).val()});
      }
      nodes = {nodes: ns}
      var companyId = $('#cid').val();
      $.ajax({
        url: "/api/answer/edit/",
        dataType: "json",
        type: "POST",
        data: {company_id: companyId, change_nodes: JSON.stringify(nodes)},
      }).done(function() {
        setTimeout(function() {location.reload();}, 0);
      }).fail(function() {
        alert('サーバー側でエラーが発生しました。しばらくしてからもう一度試してください。');
        parentModal.modal('hide');
      });
    }
  });

  /* add new question */
  $('.add-modal').click(function() {
    // refresh the input filed of add modal screen
    $('#itemName').val('');
    $('#itemType').val(1);

    $('#category').val($(this).attr('data-category'));
    $('#addTitle').html('追加: ' + $(this).attr('data-title'));
    $('#addnew').modal('show');
  });
  $('.add-submit').click(function() {
    var aType = $('#itemType').val();
    var qSentence = $('#itemName').val();
    var category = $('#category').val();
    if (aType && qSentence && category) {
      $.ajax({
        url: "/api/question/add/",
        dataType: "json",
        type: "POST",
        data: {category: category, answer_type: aType, question_sentence: qSentence},
      }).done(function() {
        setTimeout(function() {location.reload();}, 0);
      }).fail(function() {
        alert('サーバー側でエラーが発生しました。しばらくしてからもう一度試してください。');
        $('#addnew').modal('hide');
      });
    } else {
      alert('項目はすべて必須です。');
    }
  });
});
